import { useEffect, useState } from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function StudentsPage() {
  const [students, setStudents] = useState([])
  const [form, setForm] = useState({
    full_name: '',
    acca_reg_no: '',
    registration_year: '2026',
    identity_number: '',
    mobile: '',
    email: ''
  })

  const load = async () => {
    const res = await axios.get(`${API_URL}/students`)
    setStudents(res.data)
  }

  useEffect(() => {
    load()
  }, [])

  const submit = async (e) => {
    e.preventDefault()
    await axios.post(`${API_URL}/students`, form)
    setForm({ full_name: '', acca_reg_no: '', registration_year: '2026', identity_number: '', mobile: '', email: '' })
    load()
  }

  return (
    <>
      <div className="page-header">
        <h1>Students</h1>
      </div>

      <div className="panel" style={{ marginBottom: 24 }}>
        <h3>Add Student</h3>
        <form className="form-grid" onSubmit={submit}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(180px, 1fr))', gap: 16 }}>
            <input placeholder="Full Name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
            <input placeholder="ACCA Reg No" value={form.acca_reg_no} onChange={(e) => setForm({ ...form, acca_reg_no: e.target.value })} />
            <input placeholder="Registration Year" value={form.registration_year} onChange={(e) => setForm({ ...form, registration_year: e.target.value })} />
            <input placeholder="Identity Number" value={form.identity_number} onChange={(e) => setForm({ ...form, identity_number: e.target.value })} />
            <input placeholder="Mobile" value={form.mobile} onChange={(e) => setForm({ ...form, mobile: e.target.value })} />
            <input placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          </div>
          <button type="submit">Create Student</button>
        </form>
      </div>

      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>ACCA Reg No</th>
              <th>Year</th>
              <th>Mobile</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {students.map((student) => (
              <tr key={student.id}>
                <td>{student.full_name}</td>
                <td>{student.acca_reg_no}</td>
                <td>{student.registration_year}</td>
                <td>{student.mobile}</td>
                <td>{student.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
