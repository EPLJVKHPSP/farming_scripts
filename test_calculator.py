import os
import unittest
from unittest.mock import AsyncMock, Mock, patch

with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "123456:test-only-token"}):
    import calculator


class CalculatorTests(unittest.IsolatedAsyncioTestCase):
    async def test_calculation_awaits_result_and_returns_to_menu(self):
        update = Mock()
        update.message.reply_text = AsyncMock()
        context = Mock()
        context.user_data = {
            "crypto1_name": "asset-one", "crypto2_name": "asset-two",
            "crypto1_qty_before": 10, "crypto1_qty_after": 9,
            "crypto2_qty_before": 100, "crypto2_qty_after": 120,
            "commission": 3,
        }
        with patch.object(calculator, "get_price", side_effect=[10, 1]):
            state = await calculator.calculate_il(update, context)
        self.assertEqual(state, calculator.CRYPTO1)
        self.assertEqual(update.message.reply_text.await_count, 2)
        self.assertEqual(update.message.reply_text.await_args_list[0].args[0],
                         "The impermanent loss is: 13.0$")

    async def test_start_menu_and_cancel_are_awaited(self):
        update = Mock()
        update.message.reply_text = AsyncMock()
        context = Mock()
        self.assertEqual(await calculator.send_menu(update, context), calculator.CRYPTO1)
        self.assertEqual(await calculator.cancel(update, context), calculator.ConversationHandler.END)
        self.assertEqual(update.message.reply_text.await_count, 2)


if __name__ == "__main__":
    unittest.main()
