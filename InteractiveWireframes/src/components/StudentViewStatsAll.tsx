import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Trophy, Target } from 'lucide-react';

interface ViewStatsAllProps {
  onNavigate: (screen: Screen) => void;
}

export function ViewStatsAll({ onNavigate }: ViewStatsAllProps) {
  return (
    <WireframeContainer title="Accolades, Milestones & Total Hours">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('view-stats-menu')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Stats Menu
        </button>

        <div className="space-y-8">
          {/* Total Hours */}
          <div className="border-4 border-gray-800 p-6">
            <h3 className="text-gray-800 mb-4">Total Service Hours</h3>
            <div className="flex items-end gap-4">
              <div className="text-gray-800" style={{ fontSize: '48px' }}>42</div>
              <div className="text-gray-600 pb-2">hours completed</div>
            </div>
            <div className="mt-4 bg-gray-200 h-4 border-2 border-gray-800">
              <div className="bg-gray-800 h-full" style={{ width: '84%' }}></div>
            </div>
            <div className="flex justify-between mt-2 text-gray-600">
              <span>0 hours</span>
              <span>Next Milestone: 50 hours</span>
            </div>
          </div>

          {/* Milestones */}
          <div className="border-4 border-gray-800 p-6">
            <div className="flex items-center gap-3 mb-4">
              <Target className="w-6 h-6" />
              <h3 className="text-gray-800">Milestones</h3>
            </div>
            <div className="space-y-3">
              {[
                { name: '10 Hours Milestone', achieved: true, hours: 10 },
                { name: '20 Hours Milestone', achieved: true, hours: 20 },
                { name: '30 Hours Milestone', achieved: true, hours: 30 },
                { name: '40 Hours Milestone', achieved: true, hours: 40 },
                { name: '50 Hours Milestone', achieved: false, hours: 50 },
                { name: '60 Hours Milestone', achieved: false, hours: 60 },
                { name: '70 Hours Milestone', achieved: false, hours: 70 },
                { name: '80 Hours Milestone', achieved: false, hours: 80 },
                { name: '90 Hours Milestone', achieved: false, hours: 90 },
                { name: '100 Hours Milestone', achieved: false, hours: 100 },
              ].map((milestone, index) => (
                <div key={index} className="flex items-center gap-4 p-4 bg-gray-100 border-2 border-gray-800">
                  <div className={`w-8 h-8 border-2 border-gray-800 flex items-center justify-center ${milestone.achieved ? 'bg-green-200' : 'bg-white'}`}>
                    {milestone.achieved && <span>✓</span>}
                  </div>
                  <div className="flex-1">
                    <div className={milestone.achieved ? 'text-gray-800' : 'text-gray-400'}>
                      {milestone.name}
                    </div>
                  </div>
                  <div className="text-gray-600">{milestone.hours} hrs</div>
                </div>
              ))}
            </div>
          </div>

          {/* Accolades */}
          <div className="border-4 border-gray-800 p-6">
            <div className="flex items-center gap-3 mb-4">
              <Trophy className="w-6 h-6" />
              <h3 className="text-gray-800">Accolades Earned</h3>
            </div>
            <div className="grid grid-cols-3 gap-4">
              {[
                { name: 'Outstanding Service', date: '15/10/2025' },
                { name: 'Leadership', date: '22/10/2025' },
                { name: 'Rising Star', date: '05/11/2025' },
                { name: 'Team Player', date: '12/11/2025' },
                { name: 'Dedication', date: '20/11/2025' },
              ].map((accolade, index) => (
                <div key={index} className="border-2 border-gray-800 p-4 bg-yellow-50">
                  <div className="w-full h-20 border-2 border-gray-800 flex items-center justify-center mb-3">
                    <Trophy className="w-8 h-8" />
                  </div>
                  <div className="text-gray-800 text-center">{accolade.name}</div>
                  <div className="text-gray-600 text-center">{accolade.date}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}