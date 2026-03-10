import axios from 'axios';

const api = axios.create({
  baseURL: (process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001') + '/api',
  timeout: 30000,
});

// Core Data
export const getRoot = () => api.get('/').then(r => r.data);
export const getDatabaseStatus = () => api.get('/database/status').then(r => r.data);
export const getOccupations = (query = '', industry = '', region = '', limit = 50) =>
  api.get('/occupations', { params: { query, industry, region, limit } }).then(r => r.data);
export const getOccupationSummary = (id, jurisdiction = 'USA-Federal') =>
  api.get(`/occupations/${id}/summary`, { params: { jurisdiction } }).then(r => r.data);
export const getTasksForOccupation = (id, jurisdiction = 'USA-Federal', minScore = 0) =>
  api.get(`/tasks/occupation/${id}`, { params: { min_score: minScore, jurisdiction } }).then(r => r.data);
export const getHighAutomationTasks = (minScore = 80, jurisdiction = 'USA-Federal', limit = 50) =>
  api.get('/tasks/high-automation', { params: { min_score: minScore, jurisdiction, limit } }).then(r => r.data);
export const getComplianceBlocked = (jurisdiction = 'EU') =>
  api.get('/compliance/blocked', { params: { jurisdiction } }).then(r => r.data);
export const getIndustrySummary = (industry = '') =>
  api.get('/industries/summary', { params: { industry } }).then(r => r.data);
export const getDataSources = () => api.get('/data-sources').then(r => r.data);

// Scoring & Tools
export const getAITools = (category = '', vendor = '') =>
  api.get('/tools/ai', { params: { category, vendor } }).then(r => r.data);
export const getToolRecommendations = (taskId) =>
  api.get('/tools/recommendations', { params: { task_id: taskId } }).then(r => r.data);
export const getAutomationBlueprint = (taskId) =>
  api.get(`/automation/blueprint/${taskId}`).then(r => r.data);
export const getQuickWins = (automationType = '', limit = 10) =>
  api.get('/automation/quick-wins', { params: { automation_type: automationType, limit } }).then(r => r.data);

// ROI
export const getSalaryBenchmarks = (region = '', occupation = '') =>
  api.get('/roi/salaries', { params: { region, occupation } }).then(r => r.data);
export const getRoiAnalysis = (taskId = '', occupationId = '') =>
  api.get('/roi/analysis', { params: { task_id: taskId, occupation_id: occupationId } }).then(r => r.data);
export const calculateCustomROI = (data) =>
  api.post('/roi/calculate', data).then(r => r.data);

// Intelligence - Adoption
export const getIndustryAdoption = (industry = '') =>
  api.get('/intelligence/adoption/industry', { params: { industry } }).then(r => r.data);
export const getAdoptionVelocity = () => api.get('/intelligence/adoption/velocity').then(r => r.data);
export const getFirstMoverWindows = () => api.get('/intelligence/adoption/first-mover').then(r => r.data);
export const getCompetitiveBenchmark = () => api.get('/intelligence/adoption/benchmark').then(r => r.data);

// Intelligence - Skills
export const getSkillsAll = () => api.get('/intelligence/skills/all').then(r => r.data);
export const getSkillsDecay = (skill = '') =>
  api.get('/intelligence/skills/decay', { params: { skill } }).then(r => r.data);
export const getReskillingAll = () => api.get('/intelligence/skills/reskilling/all').then(r => r.data);
export const getReskillingHighestROI = (limit = 5) =>
  api.get('/intelligence/skills/reskilling/highest-roi', { params: { limit } }).then(r => r.data);
export const getWorkforceImpact = () => api.get('/intelligence/skills/workforce-impact').then(r => r.data);
export const getSkillsAtRisk = () => api.get('/intelligence/skills/at-risk-summary').then(r => r.data);

// Intelligence - Regulatory
export const getRegulatoryForecast = (jurisdiction = '') =>
  api.get('/intelligence/regulatory/forecast', { params: { jurisdiction } }).then(r => r.data);
export const getRegulatoryTimeline = () => api.get('/intelligence/regulatory/timeline').then(r => r.data);
export const getRegulatoryAll = () => api.get('/intelligence/regulatory/all').then(r => r.data);
export const getHighProbabilityRegulations = () =>
  api.get('/intelligence/regulatory/high-probability').then(r => r.data);

// Intelligence - Labor Arbitrage
export const getArbitrageAll = () => api.get('/intelligence/arbitrage/all').then(r => r.data);
export const getArbitrageGeographic = (region = '') =>
  api.get('/intelligence/arbitrage/geographic', { params: { region } }).then(r => r.data);
export const getAutomateNowList = () => api.get('/intelligence/arbitrage/automate-now').then(r => r.data);
export const getArbitrageCritical = () => api.get('/intelligence/arbitrage/critical').then(r => r.data);

// Intelligence - TCO
export const getTCOAll = () => api.get('/intelligence/tco/all').then(r => r.data);
export const getTCOHiddenMultipliers = () => api.get('/intelligence/tco/hidden-multipliers').then(r => r.data);
export const getTCOHighestHiddenCosts = (limit = 5) =>
  api.get('/intelligence/tco/highest-hidden-costs', { params: { limit } }).then(r => r.data);
export const getTCO5Year = (automationType = '', companySize = '') =>
  api.get('/intelligence/tco/5-year', { params: { automation_type: automationType, company_size: companySize } }).then(r => r.data);

// Intelligence - AI Timeline & Disruption
export const getAITimeline = (year = '') =>
  api.get('/intelligence/ai-timeline', { params: { year } }).then(r => r.data);
export const getDisruptionForecast = () => api.get('/intelligence/disruption').then(r => r.data);
export const getMostDisrupted = (limit = 5) =>
  api.get('/intelligence/disruption/most-disrupted', { params: { limit } }).then(r => r.data);
export const getSafestIndustries = (limit = 5) =>
  api.get('/intelligence/disruption/safest', { params: { limit } }).then(r => r.data);

// Intelligence - Vendors & ROI
export const getVendors = (category = '') =>
  api.get('/intelligence/vendors', { params: { category } }).then(r => r.data);
export const compareVendors = (category) =>
  api.get(`/intelligence/vendors/compare/${category}`).then(r => r.data);
export const getVendorRecommendations = () => api.get('/intelligence/vendors/recommend').then(r => r.data);
export const getROIBenchmarks = (companySize = '') =>
  api.get('/intelligence/roi-benchmarks', { params: { company_size: companySize } }).then(r => r.data);
export const getROICalculatorIntel = (automationType = '', companySize = '') =>
  api.get('/intelligence/roi-calculator', { params: { automation_type: automationType, company_size: companySize } }).then(r => r.data);

// Intelligence - Failure & Occupation Timeline
export const getFailureRates = (automationType = '') =>
  api.get('/intelligence/failure-rates', { params: { automation_type: automationType } }).then(r => r.data);
export const getOccupationTimeline = (occupation = '') =>
  api.get('/intelligence/occupation-timeline', { params: { occupation } }).then(r => r.data);
export const getOccupationsByRisk = (limit = 10) =>
  api.get('/intelligence/occupation-timeline/by-risk', { params: { limit } }).then(r => r.data);

// Intelligence - Leaders & Tasks
export const getAutomationLeaders = (sector = '') =>
  api.get('/intelligence/leaders', { params: { sector } }).then(r => r.data);
export const getTaskDifficulty = (task = '') =>
  api.get('/intelligence/task-difficulty', { params: { task } }).then(r => r.data);
export const getEasiestTasks = (limit = 10) =>
  api.get('/intelligence/task-difficulty/easiest', { params: { limit } }).then(r => r.data);
export const getTaskQuickWins = (maxWeeks = 8) =>
  api.get('/intelligence/task-difficulty/quick-wins', { params: { max_weeks: maxWeeks } }).then(r => r.data);

// Intelligence - Tech Radar & Industries
export const getTechRadar = (quadrant = '') =>
  api.get('/intelligence/tech-radar', { params: { quadrant } }).then(r => r.data);
export const getTechAdoptNow = () => api.get('/intelligence/tech-radar/adopt-now').then(r => r.data);
export const getAllIndustries = () => api.get('/intelligence/industries/all').then(r => r.data);
export const getIndustryRankings = () => api.get('/intelligence/industries/rankings').then(r => r.data);

// Intelligence - Dashboards & Playbooks
export const getExecutiveDashboard = () => api.get('/intelligence/executive-dashboard').then(r => r.data);
export const getEnhancedDashboard = () => api.get('/intelligence/executive-dashboard-enhanced').then(r => r.data);
export const getAutomationPressureIndex = (occupation) =>
  api.get(`/intelligence/pressure-index/${occupation}`).then(r => r.data);
export const getPlaybooks = (useCase = '') =>
  api.get('/intelligence/playbooks', { params: { use_case: useCase } }).then(r => r.data);
export const getPlaybooksSummary = () => api.get('/intelligence/playbooks/summary').then(r => r.data);

// AI Chat (builder assistant)
export const sendAIChat = (message, context = {}) =>
  api.post('/ai/chat', { message, context }).then(r => r.data);

export default api;
