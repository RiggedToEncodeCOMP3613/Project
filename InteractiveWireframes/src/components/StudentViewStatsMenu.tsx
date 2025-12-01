import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Award, Clock, FileText } from 'lucide-react';

interface ViewStatsMenuProps {
  onNavigate: (screen: Screen) => void;
}

export function ViewStatsMenu({ onNavigate }: ViewStatsMenuProps) {
  return (
    <WireframeContainer title="View Stats Menu">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('student-main')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Main Menu
        </button>

        <div>
          <h3 className="text-gray-800 mb-6">View Your Statistics</h3>
          
          <div className="grid grid-cols-1 gap-4">
            <button
              onClick={() => onNavigate('view-stats-accolades')}
              className="border-4 border-gray-800 p-6 hover:bg-gray-50 flex items-center gap-6"
            >
              <div className="w-16 h-16 border-2 border-gray-800 flex items-center justify-center flex-shrink-0">
                <Award className="w-8 h-8" />
              </div>
              <div className="text-left flex-1">
                <h4 className="text-gray-800">Accolades, Milestones & Total Hours</h4>
                <p className="text-gray-600">View your achievements and progress</p>
              </div>
              <div className="text-gray-400">→</div>
            </button>

            <button
              onClick={() => onNavigate('view-stats-pending')}
              className="border-4 border-gray-800 p-6 hover:bg-gray-50 flex items-center gap-6"
            >
              <div className="w-16 h-16 border-2 border-gray-800 flex items-center justify-center flex-shrink-0">
                <Clock className="w-8 h-8" />
              </div>
              <div className="text-left flex-1">
                <h4 className="text-gray-800">View Pending Requests</h4>
                <p className="text-gray-600">Check status of submitted hours</p>
                <div className="inline-block mt-1 px-3 py-1 bg-yellow-200 border border-gray-800">
                  <span className="text-gray-800">3 Pending</span>
                </div>
              </div>
              <div className="text-gray-400">→</div>
            </button>

            <button
              onClick={() => onNavigate('view-stats-history')}
              className="border-4 border-gray-800 p-6 hover:bg-gray-50 flex items-center gap-6"
            >
              <div className="w-16 h-16 border-2 border-gray-800 flex items-center justify-center flex-shrink-0">
                <FileText className="w-8 h-8" />
              </div>
              <div className="text-left flex-1">
                <h4 className="text-gray-800">View Request History</h4>
                <p className="text-gray-600">See all past requests and their status</p>
              </div>
              <div className="text-gray-400">→</div>
            </button>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}