# Contributing

Thanks for helping. The value of this dataset is that every row is checkable.

## Add an entry

1. Add one object to the `entries` array in `data/founders.json`.
2. Run `python3 scripts/validate.py`.
3. Open a pull request that links the sources you used.

## What counts

All three must be true:

- The founder was born outside New Zealand.
- The founder moved to New Zealand.
- The founder started or co-founded a business here.

Do not add people who were born in New Zealand to immigrant parents. They belong in the exclusions list in `README.md`.

## What evidence you need

Every entry needs at least these items:

- **Birthplace.** A biography, encyclopaedia entry, company history or reputable news article that states where the person was born.
- **Arrival.** A source that states when, or roughly when, they reached New Zealand.
- **Founding.** A source that links the person to the company and gives a founding year.

Add a news link when one exists. Prefer reporting over press releases.

## Confidence

Use `high` when the birthplace and founding are stated in a primary or company source.

Use `medium` when a single secondary source is all you have.

If a fact is unknown, use `null`. Do not guess. Say so in `notes`.

## Style

- Keep `id` kebab-case and unique.
- Write claims as one factual sentence.
- Put the source name in `source`, not in the URL field.
