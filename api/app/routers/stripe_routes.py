from fastapi import APIRouter, HTTPException, Request
from ..config import settings

router = APIRouter()

try:
	import stripe as stripe_sdk
except Exception:
	stripe_sdk = None


@router.post("/stripe/create-checkout-session")
def create_checkout_session():
	if not settings.stripe_secret_key or not settings.stripe_price_id or not stripe_sdk:
		# Mock: retour immédiat succès
		return {"session_url": "/pricing?mock=success"}
	stripe_sdk.api_key = settings.stripe_secret_key
	try:
		session = stripe_sdk.checkout.Session.create(
			mode="subscription",
			line_items=[{"price": settings.stripe_price_id, "quantity": 1}],
			success_url="http://localhost:3000/account?status=success",
			cancel_url="http://localhost:3000/pricing?status=cancel",
		)
		return {"session_url": session.url}
	except Exception as e:
		raise HTTPException(400, detail=str(e))


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
	# MVP: accepter, et considérer que l’utilisateur passe en Pro (à implémenter côté /me réel)
	return {"received": True}
