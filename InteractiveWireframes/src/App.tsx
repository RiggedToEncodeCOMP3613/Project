import { useState } from 'react';
import { LoginScreen } from './components/LoginScreen';
import { StudentMainMenu } from './components/StudentMainMenu';
import { MakeRequest } from './components/StudentMakeRequest';
import { ViewStatsMenu } from './components/StudentViewStatsMenu';
import { ViewStatsAll } from './components/StudentViewStatsAll';
import { ViewStatsPending } from './components/StudentViewStatsPending';
import { ViewStatsHistory } from './components/StudentViewStatsHistory';
import { StudentProfile } from './components/Profile';
import { ChangeUsername } from './components/ProfileChangeUsername';
import { ChangeEmail } from './components/ProfileChangeEmail';
import { ChangePassword } from './components/ProfileChangePassword';
import { StaffMainMenu } from './components/StaffMainMenu';
import { StaffPendingRequests } from './components/StaffViewPendingRequests';
import { LogHours } from './components/StaffLogHours';
import { MilestonesScreen } from './components/StaffMilestones';
import { CreateMilestone } from './components/StaffMilestonesCreate';
import { AccoladesScreen } from './components/StaffAccolades';
import { CreateAccolade } from './components/StaffAccoladesCreate';
import { AwardAccolade } from './components/StaffAccoladesAward';
import { Leaderboard } from './components/Leaderboard';
import { Navigation } from './components/Navigation';

export type Screen =
  | 'login'
  | 'student-main'
  | 'make-request'
  | 'view-stats-menu'
  | 'view-stats-accolades'
  | 'view-stats-pending'
  | 'view-stats-history'
  | 'leaderboard'
  | 'student-profile'
  | 'update-username'
  | 'update-email'
  | 'update-password'
  | 'staff-main'
  | 'staff-pending'
  | 'log-hours'
  | 'milestones'
  | 'create-milestone'
  | 'accolades'
  | 'create-accolade'
  | 'award-accolade'
  | 'staff-profile'
  | 'staff-update-username'
  | 'staff-update-email'
  | 'staff-update-password';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('login');

  const renderScreen = () => {
    switch (currentScreen) {
      case 'login':
        return <LoginScreen onNavigate={setCurrentScreen} />;
      case 'student-main':
        return <StudentMainMenu onNavigate={setCurrentScreen} />;
      case 'make-request':
        return <MakeRequest onNavigate={setCurrentScreen} />;
      case 'view-stats-menu':
        return <ViewStatsMenu onNavigate={setCurrentScreen} />;
      case 'view-stats-accolades':
        return <ViewStatsAll onNavigate={setCurrentScreen} />;
      case 'view-stats-pending':
        return <ViewStatsPending onNavigate={setCurrentScreen} />;
      case 'view-stats-history':
        return <ViewStatsHistory onNavigate={setCurrentScreen} />;
      case 'leaderboard':
        return <Leaderboard onNavigate={setCurrentScreen} />;
      case 'student-profile':
        return <StudentProfile onNavigate={setCurrentScreen} />;
      case 'update-username':
        return <ChangeUsername onNavigate={setCurrentScreen} userType="student" />;
      case 'update-email':
        return <ChangeEmail onNavigate={setCurrentScreen} userType="student" />;
      case 'update-password':
        return <ChangePassword onNavigate={setCurrentScreen} userType="student" />;
      case 'staff-main':
        return <StaffMainMenu onNavigate={setCurrentScreen} />;
      case 'staff-pending':
        return <StaffPendingRequests onNavigate={setCurrentScreen} />;
      case 'log-hours':
        return <LogHours onNavigate={setCurrentScreen} />;
      case 'milestones':
        return <MilestonesScreen onNavigate={setCurrentScreen} />;
      case 'create-milestone':
        return <CreateMilestone onNavigate={setCurrentScreen} />;
      case 'accolades':
        return <AccoladesScreen onNavigate={setCurrentScreen} />;
      case 'create-accolade':
        return <CreateAccolade onNavigate={setCurrentScreen} />;
      case 'award-accolade':
        return <AwardAccolade onNavigate={setCurrentScreen} />;
      case 'staff-profile':
        return <StudentProfile onNavigate={setCurrentScreen} isStaff />;
      case 'staff-update-username':
        return <ChangeUsername onNavigate={setCurrentScreen} userType="staff" />;
      case 'staff-update-email':
        return <ChangeEmail onNavigate={setCurrentScreen} userType="staff" />;
      case 'staff-update-password':
        return <ChangePassword onNavigate={setCurrentScreen} userType="staff" />;
      default:
        return <LoginScreen onNavigate={setCurrentScreen} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation currentScreen={currentScreen} onNavigate={setCurrentScreen} />
      <div className="pt-16">
        {renderScreen()}
      </div>
    </div>
  );
}
