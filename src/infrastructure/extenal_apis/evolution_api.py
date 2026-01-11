from src.core.config.settings import get_settings
from src.infrastructure.extenal_apis.api_base_client import ApiBaseClient

settings = get_settings()


class EvolutionApi(ApiBaseClient):
    def __init__(self) -> None:
        super().__init__(
            name='Evolution API',
            base_url=settings.EVOLUTION_API_URL,
            timeout=10,
            default_headers={
                'Content-Type': 'application/json',
                'apikey': settings.EVOLUTION_API_KEY,
            },
        )
        self.instance = settings.EVOLUTION_INSTANCE

    async def send_message_whatsapp(
        self,
        phone_number: str,
        message: str,
    ) -> dict:
        """
        Envia uma mensagem de texto via Evolution API (WhatsApp).

        Endpoint:
            POST /message/sendText/{instance}

        Payload:
            - number: telefone destino
            - text: mensagem
        """
        payload = {
            'number': phone_number,
            'text': message,
            'options': {
                'delay': 100,
                'presence': 'composing',
                'linkPreview': True,
            },
            'textMessage': {'text': message},
        }

        response = await self.request({
            'method': 'POST',
            'url': f'/message/sendText/{self.instance}',
            'json': payload,
        })

        return response.json()
