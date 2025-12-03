import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Trophy, Medal, Award } from 'lucide-react';

interface LeaderboardProps {
  onNavigate: (screen: Screen) => void;
}

export function Leaderboard({ onNavigate }: LeaderboardProps) {
  const leaderboardData = [
    { rank: 1, name: 'Alice Johnson', hours: 120, accolades: 8 },
    { rank: 2, name: 'Bob Smith', hours: 115, accolades: 7 },
    { rank: 3, name: 'Charlie Brown', hours: 110, accolades: 6 },
    { rank: 4, name: 'Diana Prince', hours: 105, accolades: 5 },
    { rank: 5, name: 'Edward Norton', hours: 100, accolades: 5 },
    { rank: 6, name: 'Fiona Green', hours: 95, accolades: 4 },
    { rank: 7, name: 'George Lucas', hours: 90, accolades: 4 },
    { rank: 8, name: 'Helen Troy', hours: 85, accolades: 3 },
    { rank: 9, name: 'Ian Fleming', hours: 80, accolades: 3 },
    { rank: 10, name: 'Julia Roberts', hours: 75, accolades: 2 },
  ];

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Trophy className="w-6 h-6 text-yellow-500" />;
      case 2:
        return <Medal className="w-6 h-6 text-gray-400" />;
      case 3:
        return <Award className="w-6 h-6 text-amber-600" />;
      default:
        return <span className="w-6 h-6 flex items-center justify-center text-gray-600 font-bold">{rank}</span>;
    }
  };

  return (
    <WireframeContainer title="Student Leaderboard">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('student-main')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Student Menu
        </button>

        <div className="border-4 border-gray-800 p-6">
          <h3 className="text-gray-800 mb-6 text-center">Top Students by Total Hours</h3>

          <div className="space-y-3">
            {leaderboardData.map((student) => (
              <div key={student.rank} className="flex items-center gap-4 p-4 bg-gray-100 border-2 border-gray-800">
                <div className="flex items-center justify-center w-12">
                  {getRankIcon(student.rank)}
                </div>
                <div className="flex-1">
                  <div className="text-gray-800 font-medium">{student.name}</div>
                </div>
                <div className="text-center">
                  <div className="text-gray-800 font-bold">{student.hours}</div>
                  <div className="text-gray-600 text-sm">hours</div>
                </div>
                <div className="text-center">
                  <div className="text-gray-800">{student.accolades}</div>
                  <div className="text-gray-600 text-sm">accolades</div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 text-center text-gray-600">
            Rankings updated daily based on total approved service hours
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}