import React, { useState } from 'react'
import LandingPage from './pages/LandingPage'
import ChatPage from './pages/ChatPage'
import DemoPage from './pages/DemoPage'

function App() {
  const [currentPage, setCurrentPage] = useState<'landing' | 'chat' | 'demo'>('landing')

  const handleStartChat = () => setCurrentPage('chat')
  const handleStartDemo = () => setCurrentPage('demo')
  const handleBackToLanding = () => setCurrentPage('landing')

  return (
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
  )
}

export default App
