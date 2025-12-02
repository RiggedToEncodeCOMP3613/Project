import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Plus, Edit, Trash2, Award } from 'lucide-react';

interface AccoladesScreenProps {
  onNavigate: (screen: Screen) => void;
}

export function AccoladesScreen({ onNavigate }: AccoladesScreenProps) {
  const accolades = [
    { id: 1, name: 'Outstanding Service', awarded: 23, personalAwarded: 5 },
    { id: 2, name: 'Leadership', awarded: 15, personalAwarded: 3 },
    { id: 3, name: 'Rising Star', awarded: 8, personalAwarded: 2 },
    { id: 4, name: 'Team Player', awarded: 12, personalAwarded: 4 },
    { id: 5, name: 'Dedication', awarded: 19, personalAwarded: 6 },
    { id: 6, name: 'Tax Fraud', awarded: 1, personalAwarded: 1 },
  ];

  return (
    <WireframeContainer title="Accolades Screen">
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
            <h3 className="text-gray-800">Manage Accolades</h3>
            <div className="flex gap-3">
              <button
                onClick={() => onNavigate('award-accolade')}
                className="flex items-center gap-2 px-4 py-2 border-2 border-gray-800 bg-white hover:bg-gray-100"
              >
                <Award className="w-4 h-4" />
                Award Accolade
              </button>
              <button
                onClick={() => onNavigate('create-accolade')}
                className="flex items-center gap-2 px-4 py-2 border-2 border-gray-800 bg-gray-800 text-white hover:bg-gray-700"
              >
                <Plus className="w-4 h-4" />
                Create New Accolade
              </button>
            </div>
          </div>

          <div className="border-2 border-gray-800">
            {/* Table Header */}
            <div className="grid grid-cols-4 gap-4 p-4 bg-gray-800 text-white">
              <div>Accolade Name</div>
              <div>Total Students Awarded</div>
              <div>Personally Awarded</div>
              <div>Actions</div>
            </div>

            {/* Table Rows */}
            {accolades.map((accolade, index) => (
              <div
                key={accolade.id}
                className={`grid grid-cols-4 gap-4 p-4 border-t-2 border-gray-800 ${
                  index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                }`}
              >
                <div className="text-gray-800">{accolade.name}</div>
                <div className="text-gray-600">{accolade.awarded}</div>
                <div className="text-gray-600">{accolade.personalAwarded}</div>
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
              <strong>About Accolades:</strong> Accolades are special awards given to students for exceptional
              service or achievements. Unlike milestones, accolades are manually awarded by staff members based
              on qualitative assessment of student contributions.
            </p>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}