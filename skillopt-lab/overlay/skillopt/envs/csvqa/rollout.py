"""CSV QA rollout: one chat_target call per item, graded by a pluggable grader."""
from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from skillopt.envs.csvqa.graders import get_grader
from skillopt.model import chat_target
from skillopt.prompts import load_prompt


def build_system(skill_content: str, answer_format: str = "") -> str:
    skill_section = f"## Skill\n{skill_content.strip()}\n\n" if skill_content.strip() else ""
    base = load_prompt("rollout_system", env="csvqa").format(skill_section=skill_section)
    if answer_format.strip():
        base += "\n## Required Answer Layout\n" + answer_format.strip() + "\n"
    return base


def build_user(question: str) -> str:
    return (
        "## Input\n"
        "The input text is everything between the <input> and </input> markers "
        "(it may be empty or whitespace-only).\n"
        f"<input>{question}</input>"
    )


def process_one(item: dict, out_root: str, skill_content: str, *, grader_name: str,
                max_completion_tokens: int, exec_timeout: int, answer_format: str = "") -> dict:
    item_id = str(item["id"])
    question = item.get("question", "")
    expected = item.get("expected", "")
    grader = get_grader(grader_name)
    result = {
        "id": item_id,
        "question": question,
        "task_description": question,
        "task_type": item.get("task_type", "default"),
        "expected": expected,
        "hard": 0,
        "soft": 0.0,
        "predicted_answer": "",
        "response": "",
        "fail_reason": "",
        "agent_ok": False,
        "n_turns": 0,
    }
    pred_dir = os.path.join(out_root, "predictions", item_id)
    os.makedirs(pred_dir, exist_ok=True)
    system = build_system(skill_content, answer_format)
    user = build_user(question)
    try:
        response, _usage = chat_target(
            system=system, user=user,
            max_completion_tokens=max_completion_tokens,
            retries=3, stage="rollout", timeout=exec_timeout,
        )
        result["response"] = response
        result["agent_ok"] = True
        result["n_turns"] = 1
        hard, soft, detail = grader(response, expected)
        result["hard"], result["soft"] = hard, soft
        from skillopt.envs.csvqa.graders import extract_answer
        result["predicted_answer"] = extract_answer(response)
        if not hard:
            result["fail_reason"] = f"wrong answer: {detail}"
        conversation = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": response},
            {"role": "system", "content": (
                f"[EVALUATION RESULT]\nInput: {question!r}\nPredicted answer: "
                f"{result['predicted_answer']!r}\nExpected: {expected!r}\nCorrect: {bool(hard)}"
            )},
        ]
        with open(os.path.join(pred_dir, "conversation.json"), "w", encoding="utf-8") as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)
    except Exception as exc:  # noqa: BLE001
        result["fail_reason"] = f"error: {type(exc).__name__}: {exc}"
    return result


def run_batch(*, items: list[dict], out_root: str, skill_content: str, grader_name: str,
              workers: int, max_completion_tokens: int, exec_timeout: int,
              answer_format: str = "") -> list[dict]:
    os.makedirs(out_root, exist_ok=True)
    results_path = os.path.join(out_root, "results.jsonl")
    done: dict[str, dict] = {}
    if os.path.exists(results_path):
        with open(results_path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done[str(r["id"])] = r
                except Exception:  # noqa: BLE001
                    pass
    pending = [it for it in items if str(it["id"]) not in done]
    results = list(done.values())
    total = len(items)
    completed = len(results)
    correct = sum(1 for r in results if r.get("hard"))
    with open(results_path, "a", encoding="utf-8") as outf, ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(process_one, it, out_root, skill_content, grader_name=grader_name,
                      max_completion_tokens=max_completion_tokens, exec_timeout=exec_timeout,
                      answer_format=answer_format): it
            for it in pending
        }
        for fut in as_completed(futs):
            res = fut.result()
            results.append(res)
            completed += 1
            correct += 1 if res.get("hard") else 0
            print(f"    [rollout] {completed}/{total} (acc={correct / completed:.3f}) id={res['id']} hard={res['hard']}", flush=True)
            outf.write(json.dumps(res, ensure_ascii=False) + "\n")
            outf.flush()
    if results and all(r.get("agent_ok") is False for r in results):
        raise RuntimeError(f"all {len(results)} rollouts failed: {results[0].get('fail_reason')}")
    return results
