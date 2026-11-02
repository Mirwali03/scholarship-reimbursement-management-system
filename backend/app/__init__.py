import { useEffect, useState } from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function ClaimsPage() {
  const [claims, setClaims] = useState([])
  const [students, setStudents] = useState([])
  const [cycles, setCycles] = useState([])
  const [form, setForm] = useState({ student_id: '', cycle_id: '', amount: '0' })

  const load = async () => {
    const [claimsRes, studentsRes, cyclesRes] = await Promise.all([
      axios.get(`${API_URL}/claims`),
      axios.get(`${API_URL}/students`),
      axios.get(`${API_URL}/cycles`)
    ])
    setClaims(claimsRes.data)
    setStudents(studentsRes.data)
    setCycles(cyclesRes.data)
  }

  useEffect(() => {
    load()
  }, [])

  const submit = async (e) => {
    e.preventDefault()
    await axios.post(`${API_URL}/claims`, { ...form, amount: Number(form.amount) })
    setForm({ student_id: '', cycle_id: '', amount: '0' })
    load()
  }

  return (
    <>
      <div className="page-header">
        <h1>Claims</h1>
      </div>

      <div className="panel" style={{ marginBottom: 24 }}>
        <h3>New Claim</h3>
        <form className="form-grid" onSubmit={submit}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(180px, 1fr))', gap: 16 }}>
            <select value={form.student_id} onChange={(e) => setForm({ ...form, student_id: e.target.value })}>
              <option value="">Select Student</option>
              {students.map((student) => (
                <option key={student.id} value={student.id}>{student.full_name}</option>
              ))}
            </select>
            <select value={form.cycle_id} onChange={(e) => setForm({ ...form, cycle_id: e.target.value })}>
              <option value="">Select Cycle</option>
              {cycles.map((cycle) => (
                <option key={cycle.id} value={cycle.id}>{cycle.name}</option>
              ))}
            </select>
            <input placeholder="Amount" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} />
          </div>
          <button type="submit">Create Claim</button>
        </form>
      </div>

      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Claim ID</th>
              <th>Student</th>
              <th>Cycle</th>
              <th>Status</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {claims.map((claim) => (
              <tr key={claim.id}>
                <td>{claim.id}</td>
                <td>{claim.student_name}</td>
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
