import requests
import json

from typing import Optional, Any, List
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun

from config import yaml_config

class QianFan(LLM):
    API_KEY = yaml_config["QianFanModel"]["API_KEY"]
    SECRET_KEY = yaml_config["QianFanModel"][
        "SECRET_KEY"
    ]

    def get_access_token(self):
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.API_KEY}&client_secret={self.SECRET_KEY}"

        payload = json.dumps("")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

    def get_result(self, prompt):

        url = (
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token="
            + self.get_access_token()
        )
        data = {
            "messages": [
                {"role": "user", "content": prompt},
            ]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=data)

        result = response.json()

        return result["result"]

    @property
    def _llm_type(self) -> str:
        return "QianFan"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        callbacks: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        text = self.get_result(prompt)
        return text