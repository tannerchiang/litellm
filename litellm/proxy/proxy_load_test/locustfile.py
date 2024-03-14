from locust import HttpUser, task, between, events
import json
import time


class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def chat_completion(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer sk-mh3YNUDs1d_f6fMXfvEqBA",
            # Include any additional headers you may need for authentication, etc.
        }

        # Customize the payload with "model" and "messages" keys
        payload = {
            "model": "fake-openai-endpoint",
            "messages": [
                {"role": "system", "content": "You are a chat bot."},
                {"role": "user", "content": "Hello, how are you?"},
            ],
            # Add more data as necessary
        }

        # Make a POST request to the "chat/completions" endpoint
        response = self.client.post("chat/completions", json=payload, headers=headers)

        # Print or log the response if needed

    @task(10)
    def health_readiness(self):
        start_time = time.time()
        response = self.client.get("health/readiness")
        response_time = time.time() - start_time
        if response_time > 1:
            events.request_failure.fire(
                request_type="GET",
                name="health/readiness",
                response_time=response_time,
                exception=None,
                response=response,
            )

    @task(10)
    def health_liveliness(self):
        start_time = time.time()
        response = self.client.get("health/liveliness")
        response_time = time.time() - start_time
        if response_time > 1:
            events.request_failure.fire(
                request_type="GET",
                name="health/liveliness",
                response_time=response_time,
                exception=None,
                response=response,
            )

    # @task
    # def key_generate(self):
    #     headers = {
    #         "Authorization": "Bearer sk-1234",
    #         "Content-Type": "application/json",
    #     }

    #     payload = {
    #         "models": ["gpt-3.5-turbo", "gpt-4", "claude-2"],
    #         "duration": "20m",
    #         "metadata": {"user": "ishaan@berri.ai"},
    #         "team_id": "core-infra",
    #         "max_budget": 10,
    #         "soft_budget": 5,
    #     }

    #     response = self.client.post("key/generate", json=payload, headers=headers)

    #     if response.status_code == 200:
    #         key_response = response.json()
    #         models = key_response.get("models", [])
    #         if models:
    #             # Use the first model from the key generation response to make a chat completions request
    #             model_to_use = models[0]
    #             chat_payload = {
    #                 "model": model_to_use,
    #                 "messages": [
    #                     {"role": "system", "content": "You are a chat bot."},
    #                     {"role": "user", "content": "Hello, how are you?"},
    #                 ],
    #             }
    #             chat_response = self.client.post("chat/completions", json=chat_payload, headers=headers)
    #             # Print or log the chat response if needed
