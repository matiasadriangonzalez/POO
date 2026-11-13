export function PageHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="page-header">
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </div>
  )
}
