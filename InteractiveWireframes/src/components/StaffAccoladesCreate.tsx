import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft } from 'lucide-react';

interface CreateAccoladeProps {
  onNavigate: (screen: Screen) => void;
}

export function CreateAccolade({ onNavigate }: CreateAccoladeProps) {
  return (
    <WireframeContainer title="Accolades > Create">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('accolades')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Accolades
        </button>

        <div className="max-w-2xl">
          <h3 className="text-gray-800 mb-6">Create New Accolade</h3>

          <div className="space-y-4">
            <div>
              <label className="block mb-2 text-gray-600">Accolade Name</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter accolade name (e.g., "Community Champion")</span>
              </div>
            </div>
          </div>

          <div className="flex gap-4 mt-8">
            <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700">
              Create Accolade
            </button>
            <button 
              onClick={() => onNavigate('accolades')}
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