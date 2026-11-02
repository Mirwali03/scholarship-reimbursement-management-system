import { useEffect, useState } from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const res = await axios.get(`${API_URL}/dashboard/summary`)
        setSummary(res.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading || !summary) return <div>Loading dashboard...</div>

  return (
    <>
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>

      <div className="card-grid">
        <div className="metric-card">
          <h3>Total Students</h3>
          <strong>{summary.students}</strong>
        </div>
        <div className="metric-card">
          <h3>Open Claims</h3>
          <strong>{summary.open_claims}</strong>
        </div>
        <div className="metric-card">
          <h3>Approved Claims</h3>
          <strong>{summary.approved_claims}</strong>
        </div>
        <div className="metric-card">
          <h3>Total Paid</h3>
          <strong>{summary.total_paid}</strong>
        </div>
      </div>

      <div className="panel">
        <h3>Recent Claims</h3>
        <table>
          <thead>
            <tr>
              <th>Student</th>
              <th>Cycle</th>
              <th>Status</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {summary.recent_claims.map((claim) => (
              <tr key={claim.id}>
                <td>{claim.student}</td>
                <td>{claim.cycle_name}</td>
                <td><span className="badge">{claim.status}</span></td>
                <td>{claim.amount}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
