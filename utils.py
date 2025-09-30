
import MODEL_ID from config,

def get_explanation(question_text, answer_text, model_id=BEDROCK_INFERENCE_PROFILE_ARN):
    """
    question과 answer를 기반으로 Bedrock 모델에게 explanation 요청
    """ 
    prompt = f"""You are a guide that analyzes a set of questions for the OOO certification and provides explanations.
    Most of the people attempting these questions are Data Engineers, so concepts and terminology related to Machine Learning might be unfamiliar to them.
    I will provide you with the Question and Answer.
    Explain the reasoning behind the answer so that people could understand easily.
    Please respond in Korean.
    """

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.0,
    })

    response = bedrock_client.invoke_model(
        modelId=model_id,
        contentType='application/json',
        accept='application/json',
        body=body   
    )

    response_body = json.loads(response.get('body').read())

    return  response_body['content'][0]['text']
