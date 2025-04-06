import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper, 
  CircularProgress,
  Snackbar,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Card,
  CardContent,
  AppBar,
  Toolbar,
  IconButton
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MenuIcon from '@mui/icons-material/Menu';
import RefreshIcon from '@mui/icons-material/Refresh';
import DescriptionIcon from '@mui/icons-material/Description';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('info');

  // Initialize the application
  useEffect(() => {
    // Check if API is available
    axios.get(`${API_URL}/health`)
      .then(() => {
        // Get document list
        getDocuments();
        // Check if knowledge base is initialized
        initializeKnowledgeBase(false);
      })
      .catch(err => {
        console.error('Error connecting to API:', err);
        setError('Could not connect to the backend service. Please check if it is running.');
        setInitializing(false);
      });
  }, []);

  // Get list of documents
  const getDocuments = async () => {
    try {
      const response = await axios.get(`${API_URL}/documents`);
      if (response.data.status === 'success') {
        setDocuments(response.data.documents);
      }
    } catch (err) {
      console.error('Error fetching documents:', err);
      showSnackbar('Error fetching document list', 'error');
    }
  };

  // Initialize or refresh the knowledge base
  const initializeKnowledgeBase = async (forceRefresh = false) => {
    setInitializing(true);
    try {
      const response = await axios.post(`${API_URL}/initialize`, { force_refresh: forceRefresh });
      if (response.data.status === 'success') {
        showSnackbar(
          forceRefresh ? 'Knowledge base refreshed successfully' : 'Knowledge base initialized successfully', 
          'success'
        );
      }
    } catch (err) {
      console.error('Error initializing knowledge base:', err);
      showSnackbar('Error initializing knowledge base', 'error');
    } finally {
      setInitializing(false);
    }
  };

  // Handle query submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setAnswer('');
    setSources([]);
    
    try {
      const response = await axios.post(`${API_URL}/query`, { query });
      if (response.data.status === 'success') {
        setAnswer(response.data.answer);
        setSources(response.data.sources || []);
      } else {
        showSnackbar(response.data.message || 'Error getting answer', 'error');
      }
    } catch (err) {
      console.error('Error submitting query:', err);
      showSnackbar('Error submitting query', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Show snackbar message
  const showSnackbar = (message, severity = 'info') => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setOpenSnackbar(true);
  };

  // Handle snackbar close
  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            UAE Transfer Pricing Knowledge Agent
          </Typography>
          <Button 
            color="inherit" 
            onClick={() => initializeKnowledgeBase(true)}
            startIcon={<RefreshIcon />}
            disabled={initializing}
          >
            Refresh KB
          </Button>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        {error ? (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        ) : initializing ? (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', my: 4 }}>
            <CircularProgress />
            <Typography variant="h6" sx={{ mt: 2 }}>
              Initializing Knowledge Base...
            </Typography>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Ask a question about UAE Transfer Pricing regulations
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  This knowledge agent is trained on the UAE Corporate Tax Guide for Transfer Pricing. 
                  You can ask questions about transfer pricing regulations, documentation requirements, 
                  arm's length principle, and more.
                </Typography>
                <form onSubmit={handleSubmit}>
                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <TextField
                      fullWidth
                      label="Ask a question"
                      variant="outlined"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      disabled={loading}
                    />
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      disabled={loading || !query.trim()}
                      endIcon={<SendIcon />}
                    >
                      Ask
                    </Button>
                  </Box>
                </form>
              </CardContent>
            </Card>

            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
                <CircularProgress />
              </Box>
            ) : answer ? (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Answer:
                  </Typography>
                  <Paper elevation={0} sx={{ p: 2, bgcolor: '#f5f5f5' }}>
                    <ReactMarkdown>{answer}</ReactMarkdown>
                  </Paper>

                  {sources.length > 0 && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="h6" gutterBottom>
                        Sources:
                      </Typography>
                      <List>
                        {sources.map((source, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <DescriptionIcon />
                            </ListItemIcon>
                            <ListItemText
                              primary={source.metadata.source || "Document"}
                              secondary={`Page ${source.metadata.page || "unknown"}`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}
                </CardContent>
              </Card>
            ) : null}

            {documents.length > 0 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Knowledge Base Documents:
                  </Typography>
                  <List>
                    {documents.map((doc, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <DescriptionIcon />
                        </ListItemIcon>
                        <ListItemText primary={doc} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            )}
          </Box>
        )}
      </Container>

      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </div>
  );
}

export default App;