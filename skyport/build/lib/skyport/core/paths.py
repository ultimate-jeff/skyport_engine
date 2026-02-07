
import datetime
import os
import json
from pathlib import Path
import pygame
pygame.init()

ENGINE_ROOT = Path(__file__).resolve().parent.parent

class PathUtil:
    @staticmethod
    def fp(relative_path: str) -> Path:
        p = Path(relative_path)
        if p.is_absolute():
            return p
        return (ENGINE_ROOT / p).resolve()

class ENG_Loger:
    ENGINE_LOG_PATH = PathUtil.fp("logs/engine_logs.json")
    if not os.path.exists(ENGINE_LOG_PATH):
        with open(ENGINE_LOG_PATH,"w") as f:
            json.dump({"total_logs": 5,"record_engine_logs": True,"logs": []},indent=4)
    with open(ENGINE_LOG_PATH,"r") as f:
        log_file = json.load(f)
    take_logs = log_file["record_engine_logs"]
    log_data_retaintion_amount = 5
    print(f"--engine logging is set to {take_logs}--")
    def __init__(self):
        self.log_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.run_time_log = ""
        if ENG_Loger.take_logs:
            self.log = self._true_log
        else:
            self.log = self._false_log

    def save(self):
        ENG_Loger.log_file["logs"].append({
            "log_start_time":self.log_start_time,
            "log_end_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "run_time_log":self.run_time_log
        })
        if len(ENG_Loger.log_file["logs"]) > ENG_Loger.log_data_retaintion_amount:
            ENG_Loger.log_file["logs"].pop(0)
            ENG_Loger.log_file["total_logs"] = ENG_Loger.log_data_retaintion_amount
        with open(ENG_Loger.ENGINE_LOG_PATH,"w") as f:
            json.dump(ENG_Loger.log_file,f,indent=4)
    def print(self):
        for log in ENG_Loger.log_file["logs"]:
            for line in log["run_time_log"].split("\n"):
                print(line)
            print("----- end of log")

    def _true_log(self,message):
        self.run_time_log += f"[{datetime.datetime.now().strftime('%H:%M:%S')}] :-: {message}\n"
    def _false_log(self,message):
        pass

loger = ENG_Loger()
