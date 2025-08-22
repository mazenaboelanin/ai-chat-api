def map_ai_agent_request_data(data):

  mapped_data = data.copy()
  mapped_data["stream"] = False

  if "question" in mapped_data:
    mapped_data["prompt"] = mapped_data.pop("question")

  if "user_id" in mapped_data:
    mapped_data.pop("user_id")

  return mapped_data