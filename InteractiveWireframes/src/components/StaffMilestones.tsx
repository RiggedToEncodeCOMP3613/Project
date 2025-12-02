import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Plus, Edit, Trash2 } from 'lucide-react';

interface MilestonesScreenProps {
  onNavigate: (screen: Screen) => void;
}

export function MilestonesScreen({ onNavigate }: MilestonesScreenProps) {
  const milestones = [
    { id: 1, name: '10 Hours Milestone', hours: 10 },
    { id: 2, name: '20 Hours Milestone', hours: 20 },
    { id: 3, name: '30 Hours Milestone', hours: 30 },
    { id: 4, name: '40 Hours Milestone', hours: 40 },
    { id: 5, name: '50 Hours Milestone', hours: 50 },
    { id: 6, name: '60 Hours Milestone', hours: 60 },
    { id: 7, name: '70 Hours Milestone', hours: 70 },
    { id: 8, name: '80 Hours Milestone', hours: 80 },
    { id: 9, name: '90 Hours Milestone', hours: 90 },
    { id: 10, name: '100 Hours Milestone', hours: 100 },
  ];

  return (
    <WireframeContainer title="Milestones Screen">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('staff-main')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Main Menu
        </button>

        <div>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-gray-800">Manage Milestones</h3>
            <button
              onClick={() => onNavigate('create-milestone')}
              className="flex items-center gap-2 px-4 py-2 border-2 border-gray-800 bg-gray-800 text-white hover:bg-gray-700"
            >
              <Plus className="w-4 h-4" />
              Create New Milestone
            </button>
          </div>

          <div className="border-2 border-gray-800">
            {/* Table Header */}
            <div className="grid grid-cols-3 gap-4 p-4 bg-gray-800 text-white">
              <div>Hours Required</div>
              <div>Students Achieved</div>
              <div>Actions</div>
            </div>

            {/* Table Rows */}
            {milestones.map((milestone, index) => (
              <div 
                key={milestone.id}
                className={`grid grid-cols-3 gap-4 p-4 border-t-2 border-gray-800 ${
                  index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                }`}
              >
                <div className="text-gray-600">{milestone.hours} hours</div>
                <div className="text-gray-600">
                  {milestone.hours === 10 ? 45 :
                   milestone.hours === 20 ? 40 :
                   milestone.hours === 30 ? 35 :
                   milestone.hours === 40 ? 30 :
                   milestone.hours === 50 ? 25 :
                   milestone.hours === 60 ? 20 :
                   milestone.hours === 70 ? 15 :
                   milestone.hours === 80 ? 10 :
                   milestone.hours === 90 ? 8 :
                   milestone.hours === 100 ? 5 :
                   milestone.hours === 200 ? 2 : 0}
                </div>
                <div className="flex gap-2">
                  <button className="p-2 border-2 border-gray-800 bg-white hover:bg-gray-100" title="Edit">
                    <Edit className="w-4 h-4" />
                  </button>
                  <button className="p-2 border-2 border-gray-800 bg-red-200 hover:bg-red-300" title="Delete">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-gray-100 border-2 border-gray-800">
            <p className="text-gray-800">
              <strong>About Milestones:</strong> Milestones are automatically awarded to students when they reach 
              the specified number of service hours. Students can view their progress toward each milestone.
            </p>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}