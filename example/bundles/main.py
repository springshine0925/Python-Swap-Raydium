import asyncio
import os

from bxsolana_trader_proto import api as proto

from bxsolana.transaction import signing

from bxsolana import provider

# TODO: Add some logic here to indicate to user if missing needed environment variables for tests
public_key = os.getenv("PUBLIC_KEY") #or ""
private_key =os.getenv("PRIVATE_KEY") #or  ""
base_token_wallet = os.getenv("PUBLIC_KEY") #or""

async def main():
    print("public_key", public_key)
    print("private_key", private_key)
    print("public_key", public_key)
    await http()


async def http():
    print("\n*** HTTP Start Working ***\n")
    async with provider.HttpProvider() as api:
        raydium_bundle_tx = await api.post_raydium_swap(
            proto.PostRaydiumSwapRequest(
                owner_address=public_key,
                in_token="SOL",
                out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                slippage=0.3,
                in_amount=0.03,
                tip=3000000,

            )
        )

        print(
            "created RAYDIUM swap tx with bundle tip of 1030:"
            f" {raydium_bundle_tx.transactions[0].content}"
        )

        signed_tx = signing.sign_tx(raydium_bundle_tx.transactions[0].content)

        post_submit_response = await api.post_submit(
            post_submit_request=proto.PostSubmitRequest(
                transaction=proto.TransactionMessage(content=signed_tx),
                skip_pre_flight=True,
                front_running_protection=True,
            )
        )

        print(
            "submitted RAYDIUM tx with front running protection:"
            f" {post_submit_response.signature}"
        )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())