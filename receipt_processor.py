from openai import OpenAI
from typing import List, Dict
import json
import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Configura client OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY non trovata nelle variabili d'ambiente")

def process_receipts(base64_images: List[str]) -> List[Dict]:
    # Inizializza il client OpenAI senza configurazioni aggiuntive
    client = OpenAI()  # Usa solo le configurazioni di base
    results = []
    
    for image in base64_images:
        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",  # Aggiornato il modello a quello corretto per la visione
                messages=[
                    {
                        "role": "system",
                        "content": "Leggi lo scontrino fornito e restituisci solo un JSON"
                    },
                    {
                        "role": "user",
                        "content": [
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
                            "description": "Estrae i dati di uno scontrino",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "societa": {"type": "string", "description": "La società che ha emesso lo scontrino"},
                                    "indirizzo": {"type": "string", "description": "L'indirizzo riportato sullo scontrino"},
                                    "totale": {"type": "number", "description": "Totale dello scontrino"},
                                    "imponibile": {"type": "number", "description": "Parte imponibile dello scontrino"},
                                    "iva": {"type": "number", "description": "IVA calcolata sullo scontrino"},
                                    "totale_contanti": {"type": "number", "description": "Pagato in contanti"},
                                    "totale_electronic": {"type": "number", "description": "Pagato con metodi elettronici"},
                                    "totale_non_risc": {"type": "number", "description": "Totale non riscosso"},
                                    "totale_sconto": {"type": "number", "description": "Totale sconto applicato"},
                                    "documenti_commerciali": {"type": "integer", "description": "Numero di documenti commerciali"},
                                    "matricola": {"type": "string", "description": "Matricola del dispositivo/sistema"},
                                    "data": {"type": "string", "description": "Data dello scontrino in formato ISO"},
                                    "ora": {"type": "string", "description": "Ora dello scontrino in formato HH:MM"},
                                    "documento_gestionale": {"type": "integer", "description": "Indicatore documento gestionale"}
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
                temperature=0.22,
                max_tokens=2048
            )
            
            tool_call = response.choices[0].message.tool_calls[0]
            receipt_data = json.loads(tool_call.function.arguments)
            results.append(receipt_data)
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise
    
    return results