# Continuous Memory Log

*No entries yet. Add complex bugs, workarounds, and architectural decisions here.*

## 2026-06-19: False Positive Due to Foil Cards
**Bug**: The bot reported new games like *Atomfall* as highly profitable. This happened because the Steam Market API search (`category_753_item_class[]: tag_item_class_2`) returned both normal and "Foil" trading cards. A single Foil card listed at a huge price (e.g. $100) drastically inflated the calculated `average_card_price` across the 10 results.
**Solution**: Appended `"category_753_cardborder[]": "tag_cardborder_0"` to the `marketFetcher.py` parameters to strictly exclude Foil cards from the market search, yielding a much more accurate average price.
