import fs from "node:fs";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const schema = JSON.parse(fs.readFileSync("./schema.json", "utf-8"));
const ajv = new Ajv2020({ allErrors: true, strict: true });
addFormats(ajv);
const validate = ajv.compile(schema);

const casos = [
  {
    nombre: "Caso válido",
    data: {
      procesoElectoral: "PELC 2026-2027",
      candidatura: { principio: "MR", cargo: "DIPUTACION" },
      partido: { siglas: "MC", tipoRegistro: "PARTIDO" },
      distrito: 13,
      persona: {
        nombre: "LOURDES CELENIA CONTRERAS GONZALEZ",
        curp: "ABCD010203HJCLMN09",
        fechaNacimiento: "2001-02-03",
        genero: "MUJER",
        domicilio: { municipio: "Guadalajara", cp: "44100" }
      },
      accionesAfirmativas: ["JALISCIENSE_EXTRANJERO"],
      documentos: { ine: true, actaNacimiento: true, aceptacionCandidatura: true, declaracionNoSentencia: false }
    }
  },
  {
    nombre: "Distrito fuera de rango",
    data: {
      procesoElectoral: "PELC 2026-2027",
      candidatura: { principio: "MR", cargo: "DIPUTACION" },
      partido: { siglas: "MC", tipoRegistro: "PARTIDO" },
      distrito: 30,
      persona: {
        nombre: "X",
        curp: "ABCD010203HJCLMN09",
        fechaNacimiento: "2001-02-03",
        genero: "MUJER",
        domicilio: { municipio: "Guadalajara", cp: "44100" }
      },
      documentos: { ine: true, actaNacimiento: true, aceptacionCandidatura: true }
    }
  },
  {
    nombre: "CURP inválida",
    data: {
      procesoElectoral: "PELC 2026-2027",
      candidatura: { principio: "MR", cargo: "DIPUTACION" },
      partido: { siglas: "MC", tipoRegistro: "PARTIDO" },
      distrito: 13,
      persona: {
        nombre: "PERSONA VALIDA",
        curp: "AAAA123",
        fechaNacimiento: "2001-02-03",
        genero: "MUJER",
        domicilio: { municipio: "Guadalajara", cp: "44100" }
      },
      documentos: { ine: true, actaNacimiento: true, aceptacionCandidatura: true }
    }
  }
];

for (const c of casos) {
  const ok = validate(c.data);
  console.log(`\n${c.nombre}: ${ok ? "OK" : "INVALID"}`);
  if (!ok) {
    for (const e of validate.errors ?? []) {
      console.log(`- ${e.instancePath || "(root)"}: ${e.message}`);
    }
  }
}
