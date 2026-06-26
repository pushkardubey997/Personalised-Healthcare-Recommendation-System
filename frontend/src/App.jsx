import { useState, useEffect } from 'react'
import { fetchFeatures, predictDisease } from './api/client'
import SymptomSelector from './components/SymptomSelector'
import PredictionResult from './components/PredictionResult'
import './App.css'

function App() {
  const [features, setFeatures] = useState([])
  const [selectedSymptoms, setSelectedSymptoms] = useState([])
  const [loadingFeatures, setLoadingFeatures] = useState(true)
  const [predicting, setPredicting] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadFeatures = async () => {
      try {
        const { data } = await fetchFeatures()
        setFeatures(data.features)
      } catch (err) {
        setError('Failed to load symptoms. Please ensure backend is running.')
        console.error(err)
      } finally {
        setLoadingFeatures(false)
      }
    }
    loadFeatures()
  }, [])

  const handlePredict = async () => {
    if (selectedSymptoms.length === 0) {
      setError('Please select at least one symptom.')
      return
    }

    setPredicting(true)
    setError(null)

    try {
      // Convert selected symptoms to binary vector of length 605
      const vector = features.map(f => selectedSymptoms.includes(f) ? 1 : 0)
      const { data } = await predictDisease(vector)
      setResult(data)
    } catch (err) {
      setError('Failed to predict disease. Please try again.')
      console.error(err)
    } finally {
      setPredicting(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setSelectedSymptoms([])
    setError(null)
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">
          <span className="icon">⚕️</span>
          <h1>HealthAI Predictor</h1>
        </div>
        <p className="subtitle">AI-powered disease prediction and health recommendations</p>
      </header>

      <main className="main-content">
        {error && <div className="error-banner">{error}</div>}

        {!result ? (
          <div className="prediction-form glass-panel">
            <h2>What are your symptoms?</h2>
            <p className="instruction">Select all symptoms you are currently experiencing to get an accurate prediction.</p>
            
            {loadingFeatures ? (
              <div className="loading-spinner">
                <div className="spinner"></div>
                <p>Loading symptom database...</p>
              </div>
            ) : (
              <>
                <SymptomSelector 
                  features={features} 
                  selected={selectedSymptoms} 
                  onChange={setSelectedSymptoms} 
                />
                
                <div className="action-bar">
                  <button 
                    className={`predict-btn ${predicting ? 'loading' : ''}`}
                    onClick={handlePredict}
                    disabled={predicting || selectedSymptoms.length === 0}
                  >
                    {predicting ? 'Analyzing...' : 'Predict Disease'}
                  </button>
                </div>
              </>
            )}
          </div>
        ) : (
          <PredictionResult result={result} onReset={handleReset} />
        )}
      </main>

      <footer className="app-footer">
        <p>Disclaimer: This is an AI tool and does not replace professional medical advice.</p>
      </footer>
    </div>
  )
}

export default App
