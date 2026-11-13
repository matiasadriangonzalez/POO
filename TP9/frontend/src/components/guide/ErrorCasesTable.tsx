import { TRIGGER_LABEL, type ErrorCase } from '../../content/useCases'

export function ErrorCasesTable({ cases }: { cases: ErrorCase[] }) {
  return (
    <div className="table-wrap">
      <table className="cases">
        <thead>
          <tr>
            <th scope="col">Cómo provocarlo</th>
            <th scope="col">Dónde</th>
            <th scope="col">Respuesta</th>
          </tr>
        </thead>
        <tbody>
          {cases.map((item) => (
            <tr key={`${item.status}-${item.how}`}>
              <td>{item.how}</td>
              <td>
                <span className={`pill ${item.where}`}>{TRIGGER_LABEL[item.where]}</span>
              </td>
              <td>
                <span className="status-code">{item.status}</span> {item.message}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
