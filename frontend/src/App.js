import '@/App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/layout/Layout';
import Dashboard from '@/pages/Dashboard';
import OccupationExplorer from '@/pages/OccupationExplorer';
import SkillsIntelligence from '@/pages/SkillsIntelligence';
import RegulatoryCompliance from '@/pages/RegulatoryCompliance';
import IndustryIntelligence from '@/pages/IndustryIntelligence';
import ROICalculator from '@/pages/ROICalculator';
import VendorIntelligence from '@/pages/VendorIntelligence';
import LaborArbitrage from '@/pages/LaborArbitrage';
import BuildHome from '@/pages/BuildHome';
import BuildWizard from '@/pages/BuildWizard';
import BuildBlueprints from '@/pages/BuildBlueprints';
import BuildChat from '@/pages/BuildChat';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="occupations" element={<OccupationExplorer />} />
          <Route path="skills" element={<SkillsIntelligence />} />
          <Route path="regulatory" element={<RegulatoryCompliance />} />
          <Route path="industries" element={<IndustryIntelligence />} />
          <Route path="roi" element={<ROICalculator />} />
          <Route path="vendors" element={<VendorIntelligence />} />
          <Route path="arbitrage" element={<LaborArbitrage />} />
          <Route path="build" element={<BuildHome />} />
          <Route path="build/wizard" element={<BuildWizard />} />
          <Route path="build/blueprints" element={<BuildBlueprints />} />
          <Route path="build/chat" element={<BuildChat />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
