#!/usr/bin/env python3
"""Prepara la specifica OpenAPI per la generazione degli SDK.

- Rimuove gli schemi marcati `x-internal: true` che non sono referenziati da nessuna parte
  (tipi infrastrutturali orfani): non fanno parte del contratto pubblico e inquinerebbero
  inutilmente gli SDK. Gli schemi interni che invece sono referenziati (es. body di una
  richiesta) vengono mantenuti, per non rompere i `$ref`.
- Rimuove l'estensione vendor `x-internal` dagli schemi che restano (i generator non la usano).
- Con `--senza-minlength-obbligatori` toglie `minLength: 1` dalle proprietà stringa. Serve all'SDK
  Python, l'unico che valida anche le risposte: un testo obbligatorio che il client Windows ha
  lasciato vuoto arriva come `""` e farebbe fallire l'intera lista
  (CIR2000/Amica20.WebApi.CustomerService#36). In scrittura il server rifiuta comunque la stringa
  vuota con un 400.

Uso: python clean_openapi_for_sdk.py <input.json> <output.json> [--senza-minlength-obbligatori]
"""
import json
import re
import sys


def collect_refs(obj, refs):
    """Raccoglie i nomi degli schemi referenziati via $ref in `obj`."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref" and isinstance(value, str):
                match = re.fullmatch(r"#/components/schemas/(.+)", value)
                if match:
                    refs.add(match.group(1))
            else:
                collect_refs(value, refs)
    elif isinstance(obj, list):
        for item in obj:
            collect_refs(item, refs)


def remove_min_length_one(obj):
    """Toglie `minLength: 1` dalle stringhe in `obj`; restituisce quante ne ha tolte."""
    removed = 0
    if isinstance(obj, dict):
        if obj.get("type") == "string" and obj.get("minLength") == 1:
            del obj["minLength"]
            removed += 1
        for value in obj.values():
            removed += remove_min_length_one(value)
    elif isinstance(obj, list):
        for item in obj:
            removed += remove_min_length_one(item)
    return removed


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 2 or flags - {"--senza-minlength-obbligatori"}:
        print("uso: clean_openapi_for_sdk.py <input.json> <output.json> [--senza-minlength-obbligatori]",
              file=sys.stderr)
        sys.exit(2)

    with open(args[0], encoding="utf-8") as f:
        spec = json.load(f)

    schemas = spec.get("components", {}).get("schemas", {})
    internal = {name for name, s in schemas.items() if isinstance(s, dict) and s.get("x-internal") is True}

    # Schemi referenziati da paths e dagli schemi NON interni.
    used = set()
    collect_refs(spec.get("paths", {}), used)
    for name, schema in schemas.items():
        if name not in internal:
            collect_refs(schema, used)

    # Rimuove gli schemi interni orfani (non referenziati).
    removed = [name for name in internal if name not in used]
    for name in removed:
        del schemas[name]

    # Rimuove l'estensione x-internal dagli schemi rimasti.
    for schema in schemas.values():
        if isinstance(schema, dict):
            schema.pop("x-internal", None)

    if "--senza-minlength-obbligatori" in flags:
        print(f"minLength: 1 rimossi: {remove_min_length_one(schemas)}")

    with open(args[1], "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)

    print(f"Schemi interni orfani rimossi ({len(removed)}): {', '.join(sorted(removed)) or '-'}")
    print(f"Schemi pubblici nello spec SDK: {len(schemas)}")


if __name__ == "__main__":
    main()
