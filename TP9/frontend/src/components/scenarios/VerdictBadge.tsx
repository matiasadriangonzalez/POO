export function VerdictBadge({ passed }: { passed: boolean }) {
  return (
    <span className={passed ? 'sc-verdict pass' : 'sc-verdict fail'}>
      <span aria-hidden="true">{passed ? '✓' : '✕'}</span> {passed ? 'CUMPLE' : 'NO CUMPLE'}
    </span>
  )
}
