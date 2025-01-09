from openai import OpenAI
from typing import List, Dict
import json
import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

def process_receipts(base64_images: List[str]) -> List[Dict]:
    # Inizializza il client OpenAI nel modo più semplice possibile
    try:
        client = OpenAI()
    except Exception as e:
        print(f"Error initializing OpenAI client: {str(e)}")
        raise

    results = []
    
    for image in base64_images:
        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analizza questo scontrino e fornisci i dati in formato JSON"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image}"
                                }
                            }
                        ]
                    }
                ],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "estrazione_scontrino",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "societa": {"type": "string"},
                                    "indirizzo": {"type": "string"},
                                    "totale": {"type": "number"},
                                    "imponibile": {"type": "number"},
                                    "iva": {"type": "number"},
                                    "totale_contanti": {"type": "number"},
                                    "totale_electronic": {"type": "number"},
                                    "totale_non_risc": {"type": "number"},
                                    "totale_sconto": {"type": "number"},
                                    "documenti_commerciali": {"type": "integer"},
                                    "matricola": {"type": "string"},
                                    "data": {"type": "string"},
                                    "ora": {"type": "string"},
                                    "documento_gestionale": {"type": "integer"}
                                },
                                "required": [
                                    "societa", "indirizzo", "totale", "imponibile", "iva",
                                    "totale_contanti", "totale_electronic", "totale_non_risc",
                                    "totale_sconto", "documenti_commerciali", "matricola",
                                    "data", "ora", "documento_gestionale"
                                ]
                            }
                        }
                    }
                ],
                max_tokens=1000
            )
            
            tool_call = response.choices[0].message.tool_calls[0]
            receipt_data = json.loads(tool_call.function.arguments)
            results.append(receipt_data)
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise
    
    return results