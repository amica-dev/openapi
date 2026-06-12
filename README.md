# Amica OpenAPI

Questo repository contiene la **specifica OpenAPI** curata della [Customer API](https://customerws1.amica20.it/api/v3/docs)
di Amica ed è la sorgente da cui vengono generati gli SDK pubblici.

## Contenuto

- `openapi.json` — la specifica OpenAPI v3, aggiornata e taggata a ogni rilascio della
  Customer API.
- `scripts/clean_openapi_for_sdk.py` — prepara lo spec per la generazione degli SDK
  (rimuove i tipi interni orfani e l'estensione `x-internal`).
- `.github/workflows/sdk.yml` — genera gli SDK con [OpenAPI Generator](https://openapi-generator.tech)
  e li pubblica in un repository per linguaggio.

## SDK generati

| Linguaggio | Repository |
|------------|------------|
| C# / .NET | [`amica-dev/csharp-sdk`](https://github.com/amica-dev/csharp-sdk) |
| Python | [`amica-dev/python-sdk`](https://github.com/amica-dev/python-sdk) |
| TypeScript | [`amica-dev/typescript-sdk`](https://github.com/amica-dev/typescript-sdk) |
| PHP | [`amica-dev/php-sdk`](https://github.com/amica-dev/php-sdk) |

## Generare un client manualmente

```bash
openapi-generator-cli generate -i openapi.json -g <linguaggio> -o ./client
```

La specifica è distribuita con licenza MIT (vedi `LICENSE`).
