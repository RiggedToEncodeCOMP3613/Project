import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft } from 'lucide-react';

interface CreateMilestoneProps {
  onNavigate: (screen: Screen) => void;
}

export function CreateMilestone({ onNavigate }: CreateMilestoneProps) {
  return (
    <WireframeContainer title="Milestones Screen > Create">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('milestones')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Milestones
        </button>

        <div className="max-w-2xl">
          <h3 className="text-gray-800 mb-6">Create New Milestone</h3>

          <div className="space-y-4">

            <div>
              <label className="block mb-2 text-gray-600">Hours Required</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter number of hours</span>
              </div>
              <p className="text-gray-600 mt-1">Number of service hours required to achieve this milestone</p>
            </div>
          </div>

          <div className="flex gap-4 mt-8">
            <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700">
              Create Milestone
            </button>
            <button 
              onClick={() => onNavigate('milestones')}
              className="flex-1 border-2 border-gray-800 bg-white text-gray-800 px-6 py-3 hover:bg-gray-100"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}