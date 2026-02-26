import React from 'react';
import DemoMode from '../components/DemoMode';

interface DemoPageProps {
  onExit: () => void;
}

const DemoPage: React.FC<DemoPageProps> = ({ onExit }) => {
  return <DemoMode onExit={onExit} />;
};

export default DemoPage;
