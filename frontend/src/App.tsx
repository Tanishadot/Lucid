import React, { useState } from 'react'
import LandingPage from './pages/LandingPage'
import ChatPage from './pages/ChatPage'
import DemoPage from './pages/DemoPage'
import { ThemeProvider } from './contexts/ThemeContext'
import BackgroundLayer from './components/BackgroundLayer'

function App() {
  const [currentPage, setCurrentPage] = useState<'landing' | 'chat' | 'demo'>('landing')

  const handleStartChat = () => setCurrentPage('chat')
  const handleStartDemo = () => setCurrentPage('demo')
  const handleBackToLanding = () => setCurrentPage('landing')

  return (
    <ThemeProvider>
      <BackgroundLayer />
      <div className="App">
        {currentPage === 'landing' && (
          <LandingPage 
            onStartChat={handleStartChat} 
            onStartDemo={handleStartDemo} 
          />
        )}
        {currentPage === 'chat' && (
          <ChatPage onBack={handleBackToLanding} />
        )}
        {currentPage === 'demo' && (
          <DemoPage onExit={handleBackToLanding} />
        )}
      </div>
    </ThemeProvider>
  )
}

export default App
