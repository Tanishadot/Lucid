import React from 'react';
import AtmosphericEntry from '../components/AtmosphericEntry';
import InteractiveReflection from '../components/InteractiveReflection';
import DualEntryButtons from '../components/DualEntryButtons';
import Mascot from '../components/Mascot';

interface LandingPageProps {
  onStartChat: () => void;
  onStartDemo: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onStartChat, onStartDemo }) => {
  const handlePromptClick = (prompt: string) => {
    console.log('Prompt clicked:', prompt);
  };

  return (
    <div className="min-h-screen">
      <AtmosphericEntry />
      <InteractiveReflection onPromptClick={handlePromptClick} />
      <DualEntryButtons onStartChat={onStartChat} onStartDemo={onStartDemo} />
      <div className="fixed bottom-8 right-8">
        <Mascot />
      </div>
    </div>
  );
};

export default LandingPage;
