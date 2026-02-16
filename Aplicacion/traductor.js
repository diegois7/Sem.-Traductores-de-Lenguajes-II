import fs from "node:fs";

function toJsonSchema(userSchema) {
  function convert(node) {
    if (node === null || typeof node !== "object" || Array.isArray(node)) {
      throw new Error("Nodo inválido: se esperaba un objeto JSON.");
    }

    const out = {};

    if (node.title !== undefined) out.title = node.title;

    for (const comp of ["allOf", "anyOf", "oneOf", "not"]) {
      if (node[comp] !== undefined) {
        out[comp] = node[comp].map((x) =>
          typeof x === "object" && x !== null ? convert(x) : x
        );
      }
    }

    const t = node.type;
    if (t !== undefined) out.type = t;

    if (t === "object") {
      const props = node.properties ?? {};
      const outProps = {};
      for (const [k, v] of Object.entries(props)) outProps[k] = convert(v);
      out.properties = outProps;

      if (node.required !== undefined) out.required = [...node.required];

      out.additionalProperties = Boolean(node.additionalProperties ?? false);
    }

    if (t === "array") {
      if (node.items === undefined) throw new Error("type=array requiere 'items'.");
      out.items = convert(node.items);
    }

    if (t === "string") {
      if (node.min !== undefined) out.minLength = Number(node.min);
      if (node.max !== undefined) out.maxLength = Number(node.max);
      if (node.pattern !== undefined) out.pattern = node.pattern;
      if (node.format !== undefined) out.format = node.format;
    }

    if (t === "number" || t === "integer") {
      if (node.min !== undefined) out.minimum = node.min;
      if (node.max !== undefined) out.maximum = node.max;
    }

    if (node.enum !== undefined) out.enum = [...node.enum];

    return out;
  }

  const schema = convert(userSchema);
  if (schema.$schema === undefined) schema.$schema = "https://json-schema.org/draft/2020-12/schema";
  return schema;
}

const inputPath = process.argv[2] ?? "schema_iepc_candidatura.json";
const outPath = process.argv[3] ?? "schema.json";

const userSchema = JSON.parse(fs.readFileSync(inputPath, "utf-8"));
const jsonSchema = toJsonSchema(userSchema);

fs.writeFileSync(outPath, JSON.stringify(jsonSchema, null, 2), "utf-8");
