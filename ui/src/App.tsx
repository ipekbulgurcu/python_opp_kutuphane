import React, { useEffect, useMemo, useState } from 'react'
import { CssBaseline, Container, Typography, Stack, TextField, Button, Paper, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material'

type Book = { id: number; title: string; author: string; publication_year?: number | null }

const API_BASE = 'http://127.0.0.1:8000'

export default function App() {
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(false)
  const [title, setTitle] = useState('')
  const [author, setAuthor] = useState('')
  const canSubmit = useMemo(() => title.trim().length >= 3 && author.trim().length >= 2, [title, author])

  async function fetchBooks() {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/books/`)
      const data = await res.json()
      setBooks(data)
    } finally {
      setLoading(false)
    }
  }

  async function createBook() {
    if (!canSubmit) return
    const res = await fetch(`${API_BASE}/books/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, author }),
    })
    if (res.ok) {
      setTitle('')
      setAuthor('')
      fetchBooks()
    }
  }

  async function deleteBook(id: number) {
    await fetch(`${API_BASE}/books/${id}`, { method: 'DELETE' })
    fetchBooks()
  }

  useEffect(() => {
    fetchBooks()
  }, [])

  return (
    <>
      <CssBaseline />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Stack spacing={3}>
          <Typography variant="h4">Library (Material 3)</Typography>
          <Paper variant="outlined" sx={{ p: 2 }}>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <TextField label="Title" value={title} onChange={e => setTitle(e.target.value)} fullWidth />
              <TextField label="Author" value={author} onChange={e => setAuthor(e.target.value)} fullWidth />
              <Button disabled={!canSubmit} variant="contained" onClick={createBook}>Add</Button>
              <Button variant="outlined" onClick={fetchBooks} disabled={loading}>Refresh</Button>
            </Stack>
          </Paper>

          <Paper variant="outlined" sx={{ p: 2 }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Title</TableCell>
                  <TableCell>Author</TableCell>
                  <TableCell>Year</TableCell>
                  <TableCell></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {books.map(b => (
                  <TableRow key={b.id}>
                    <TableCell>{b.id}</TableCell>
                    <TableCell>{b.title}</TableCell>
                    <TableCell>{b.author}</TableCell>
                    <TableCell>{b.publication_year ?? '-'}</TableCell>
                    <TableCell>
                      <Button color="error" size="small" onClick={() => deleteBook(b.id)}>Delete</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </Stack>
      </Container>
    </>
  )
}


