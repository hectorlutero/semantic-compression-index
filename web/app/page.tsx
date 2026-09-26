"use client";

import { useState, useTransition } from "react";
import { compressText, type CompressResponse, type Level } from "@/lib/api";
import { EXAMPLES, type ExampleId } from "@/lib/examples";

export default function HomePage() {
  const [text, setText] = useState(EXAMPLES.joao.text);
  const [activeExample, setActiveExample] = useState<ExampleId>("joao");
  const [level, setLevel] = useState<Level>(1);
  const [result, setResult] = useState<CompressResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  function loadExample(id: ExampleId) {
    setActiveExample(id);
    setText(EXAMPLES[id].text);
    setError(null);
  }

  function runCompress() {
    setError(null);
    startTransition(async () => {
      try {
        const data = await compressText(text);
        setResult(data);
        document.getElementById("workspace")?.scrollIntoView({ behavior: "smooth" });
      } catch (err) {
        setResult(null);
        setError(err instanceof Error ? err.message : "Falha ao comprimir");
      }
    });
  }

  const symbolic = result?.renders?.[String(level)] ?? "";
  const glossNodes = result?.canonical?.nodes ?? [];

  return (
    <>
      <header className="topnav">
        <div className="brand">
          Logos <span>OS</span>
        </div>
        <a className="btn btn-ghost-dark" href="#workspace" style={{ height: 40 }}>
          Workspace
        </a>
      </header>

      <section className="hero">
        <div className="hero-inner">
          <p className="eyebrow reveal">DeepFlowRun · SYMBOLS v3</p>
          <h1 className="reveal-delay">Logos OS</h1>
          <p className="reveal-delay-2">
            Extraia a alma simbólica de qualquer texto — macros, categorias e
            operadores — numa interlíngua hierárquica.
          </p>
          <div className="cta-row reveal-delay-2">
            <a className="btn btn-primary" href="#workspace">
              Comprimir texto
            </a>
            <button
              type="button"
              className="btn btn-ghost-dark"
              onClick={() => {
                loadExample("joao");
                document.getElementById("workspace")?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              Ver exemplo João
            </button>
          </div>
        </div>
      </section>

      <section id="workspace" className="section muted">
        <div className="section-inner">
          <p className="eyebrow">Workspace</p>
          <h2>Cole o texto e comprima</h2>
          <p className="lede">
            O cliente fala só com o adapter HTTP do Logos Core — sem reimplementar
            extração no browser.
          </p>

          <div className="workspace-grid">
            <div className="examples" role="group" aria-label="Exemplos">
              {(Object.keys(EXAMPLES) as ExampleId[]).map((id) => (
                <button
                  key={id}
                  type="button"
                  className={`chip${activeExample === id ? " active" : ""}`}
                  onClick={() => loadExample(id)}
                >
                  {EXAMPLES[id].label}
                </button>
              ))}
            </div>

            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              aria-label="Texto de entrada"
              placeholder="Cole um texto narrativo, jurídico ou científico…"
            />

            <div>
              <button
                type="button"
                className="btn btn-primary"
                onClick={runCompress}
                disabled={pending || !text.trim()}
              >
                {pending ? "Comprimindo…" : "Comprimir"}
              </button>
              {error ? <p className="error">{error}</p> : null}
            </div>
          </div>
        </div>
      </section>

      <section className="section dark">
        <div className="section-inner">
          <p className="eyebrow">Resultado</p>
          <h2>Níveis simbólicos</h2>
          <p className="lede">
            Alterne entre macros (L1), categorias (L2) e símbolos base (L3).
          </p>

          <div className={result ? "results-enter" : undefined}>
            <div className="level-toggle" role="group" aria-label="Nível">
              {([1, 2, 3] as Level[]).map((lvl) => (
                <button
                  key={lvl}
                  type="button"
                  className={level === lvl ? "active" : ""}
                  onClick={() => setLevel(lvl)}
                >
                  L{lvl}
                </button>
              ))}
            </div>

            <div className="symbolic-pane" aria-live="polite">
              {symbolic ||
                "O painel simbólico aparece aqui após comprimir um texto."}
            </div>

            {result ? (
              <div className="meta-row">
                <span>version={result.canonical.version}</span>
                <span>
                  coverage=
                  {(result.canonical.coverage.matched_ratio * 100).toFixed(0)}%
                </span>
                <span>nodes={result.canonical.nodes.length}</span>
              </div>
            ) : null}
          </div>
        </div>
      </section>

      <section className="section light">
        <div className="section-inner">
          <p className="eyebrow">Glossário</p>
          <h2>Símbolos usados</h2>
          <p className="lede">
            Definições vindas do índice v3 interno ao Core (`describe_symbol`).
          </p>
          {glossNodes.length === 0 ? (
            <p className="lede">Comprima um texto para ver as glosas.</p>
          ) : (
            <ul className="gloss-list">
              {uniqueGloss(glossNodes).map((n) => (
                <li key={`${n.symbol}-${n.macro}`}>
                  <code>{n.symbol}</code>
                  <span>
                    <strong>{n.macro}</strong>
                    {n.category ? ` · ${n.category}` : ""}
                    {n.gloss ? ` — ${n.gloss}` : ""}
                    {n.modal ? ` [${n.modal.system}:${n.modal.operator}]` : ""}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>
    </>
  );
}

function uniqueGloss(
  nodes: CompressResponse["canonical"]["nodes"]
): CompressResponse["canonical"]["nodes"] {
  const seen = new Set<string>();
  const out: typeof nodes = [];
  for (const n of nodes) {
    if (seen.has(n.symbol)) continue;
    seen.add(n.symbol);
    out.push(n);
  }
  return out;
}
