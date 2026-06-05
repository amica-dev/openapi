# Amica OpenAPI

Questo repository contiene la **specifica OpenAPI** curata della [Customer API](https://customerws1.amica20.it/api/v3/docs)
di Amica ed è la sorgente da cui vengono generati gli SDK pubblici.

## Contenuto

- `openapi.json` — la specifica OpenAPI v3, aggiornata e taggata a ogni rilascio della
  Customer API dal workflow `openapi.yml` del repository
  [`Amica20.WebApi.CustomerService`](https://github.com/CIR2000/Amica20.WebApi.CustomerService).
- `scripts/clean_openapi_for_sdk.py` — prepara lo spec per la generazione degli SDK
  (rimuove i tipi interni orfani e l'estensione `x-internal`).
- `.github/workflows/sdk.yml` — genera gli SDK con [OpenAPI Generator](https://openapi-generator.tech)
  e li pubblica in un repository per linguaggio.

## SDK generati

| Linguaggio | Repository |
|------------|------------|
| C# / .NET | [`CIR2000/amica-csharp`](https://github.com/CIR2000/amica-csharp) |
| Python | [`CIR2000/amica-python`](https://github.com/CIR2000/amica-python) |
| TypeScript | [`CIR2000/amica-typescript`](https://github.com/CIR2000/amica-typescript) |
| PHP | [`CIR2000/amica-php`](https://github.com/CIR2000/amica-php) |

## Generare un client manualmente

```bash
openapi-generator-cli generate -i openapi.json -g <linguaggio> -o ./client
```

La specifica è distribuita con licenza MIT (vedi `LICENSE`).
