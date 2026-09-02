"""Generic CSV question/expected-answer environment for SkillOpt."""
from __future__ import annotations

from skillopt.datasets.base import BatchSpec
from skillopt.envs.base import EnvAdapter
from skillopt.envs.csvqa.dataloader import CsvQADataLoader
from skillopt.envs.csvqa.rollout import run_batch


class CsvQAAdapter(EnvAdapter):
    def __init__(self, split_dir: str = "", data_path: str = "", split_mode: str = "ratio",
                 split_ratio: str = "4:2:4", split_seed: int = 42, split_output_dir: str = "",
                 exec_timeout: int = 180, workers: int = 8, analyst_workers: int = 4,
                 failure_only: bool = False, minibatch_size: int = 8, edit_budget: int = 4,
                 seed: int = 42, limit: int = 0, max_completion_tokens: int = 4096,
                 grader: str = "exact", answer_format: str = "", gate_repeats: int = 1) -> None:
        self.exec_timeout = int(exec_timeout)
        self.workers = int(workers)
        self.analyst_workers = analyst_workers
        self.failure_only = failure_only
        self.minibatch_size = minibatch_size
        self.edit_budget = edit_budget
        self.max_completion_tokens = int(max_completion_tokens)
        self.grader = grader
        self.answer_format = answer_format
        self.gate_repeats = max(1, int(gate_repeats))
        self.dataloader = CsvQADataLoader(
            split_dir=split_dir, data_path=data_path, split_mode=split_mode,
            split_ratio=split_ratio, split_seed=split_seed,
            split_output_dir=split_output_dir, seed=seed, limit=limit,
        )

    def setup(self, cfg: dict) -> None:
        super().setup(cfg)
        self.dataloader.setup(cfg)

    def get_dataloader(self):
        return self.dataloader

    def build_env_from_batch(self, batch: BatchSpec, **kwargs):
        return list(batch.payload or [])

    def build_train_env(self, batch_size: int, seed: int, **kwargs):
        return self.build_env_from_batch(self.dataloader.build_train_batch(batch_size=batch_size, seed=seed, **kwargs))

    def build_eval_env(self, env_num: int, split: str, seed: int, **kwargs):
        return self.build_env_from_batch(self.dataloader.build_eval_batch(env_num=env_num, split=split, seed=seed, **kwargs))

    def _run(self, items, skill_content: str, out_dir: str) -> list[dict]:
        return run_batch(items=items, out_root=out_dir, skill_content=skill_content,
                         grader_name=self.grader, workers=self.workers,
                         max_completion_tokens=self.max_completion_tokens,
                         exec_timeout=self.exec_timeout, answer_format=self.answer_format)

    def rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs) -> list[dict]:
        import json
        import os
        is_gate_eval = os.path.basename(os.path.normpath(out_dir)).startswith("selection_eval")
        if not is_gate_eval or self.gate_repeats == 1:
            return self._run(env_manager, skill_content, out_dir)
        # Repeated validation: run the gate set K times and report per-item
        # mean hard/soft, so the gate compares averages instead of one noisy draw.
        reps = [self._run(env_manager, skill_content, os.path.join(out_dir, f"rep_{k + 1}"))
                for k in range(self.gate_repeats)]
        by_id: dict[str, list[dict]] = {}
        for run in reps:
            for r in run:
                by_id.setdefault(str(r["id"]), []).append(r)
        merged: list[dict] = []
        for item_id, rs in by_id.items():
            base = dict(rs[0])
            base["hard"] = sum(float(r.get("hard", 0)) for r in rs) / len(rs)
            base["soft"] = sum(float(r.get("soft", 0.0)) for r in rs) / len(rs)
            base["hard_runs"] = [float(r.get("hard", 0)) for r in rs]
            base["fail_reason"] = "; ".join(r.get("fail_reason", "") for r in rs if r.get("fail_reason"))
            merged.append(base)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "results.jsonl"), "w", encoding="utf-8") as f:
            for r in merged:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        n = len(merged) or 1
        print(f"    [gate-repeats] K={self.gate_repeats} mean hard={sum(r['hard'] for r in merged) / n:.4f} "
              f"per-run={[round(sum(float(r.get('hard', 0)) for r in run) / n, 4) for run in reps]}", flush=True)
        return merged

    def get_task_types(self) -> list[str]:
        seen: list[str] = []
        for item in self.dataloader.train_items + self.dataloader.val_items + self.dataloader.test_items:
            tt = str(item.get("task_type") or "default")
            if tt not in seen:
                seen.append(tt)
        return seen or ["default"]
