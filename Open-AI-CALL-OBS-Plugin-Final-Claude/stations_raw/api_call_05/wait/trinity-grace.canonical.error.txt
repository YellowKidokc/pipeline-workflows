Job failed at 2026-06-28 15:15:55
Error: RuntimeError: No API key found for provider 'openai'.
Add one to keys.txt (key name: OPENAI_API_KEY) or set the environment variable.
Get a key at: https://platform.openai.com/api-keys

Traceback (most recent call last):
  File "D:\GitHub\Open-AI-CALL-claude-multi-api-batch-processor-d0fcwr\core\worker.py", line 255, in do_job
    result = api_client.call(
             ^^^^^^^^^^^^^^^^
  File "D:\GitHub\Open-AI-CALL-claude-multi-api-batch-processor-d0fcwr\core\api_client.py", line 220, in call
    raise RuntimeError(
RuntimeError: No API key found for provider 'openai'.
Add one to keys.txt (key name: OPENAI_API_KEY) or set the environment variable.
Get a key at: https://platform.openai.com/api-keys

