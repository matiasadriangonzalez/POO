import { SWAGGER_URL, USEFUL_DATA } from '../../content/useCases'

export function UsefulData() {
  return (
    <section className="card" aria-labelledby="useful-data">
      <h3 id="useful-data">Datos útiles</h3>
      <dl className="useful">
        {USEFUL_DATA.map((item) => (
          <div key={item.label}>
            <dt>{item.label}</dt>
            <dd>
              {item.code && <code>{item.code}</code>} {item.text}
            </dd>
          </div>
        ))}
      </dl>
      <p>
        <a href={SWAGGER_URL} target="_blank" rel="noopener noreferrer">
          Abrir Swagger ({SWAGGER_URL})
        </a>{' '}
        <span className="muted">para los casos de error que la UI no permite enviar.</span>
      </p>
    </section>
  )
}
