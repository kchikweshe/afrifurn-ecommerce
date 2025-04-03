import { Category, Color, Currency, Level1Category, Level2Category, Material } from '@/types';

export type State = {

  mainCategories: Category[];
  levelTwoCategories: Level2Category[];
  levelOneCategories: Level1Category[];
  currencies: Currency[];
  colors: Color[];
  materials: Material[];
  loading: boolean;
  error: string | null;
};



type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Partial<State> }
  | { type: 'FETCH_ERROR'; payload: string };

export function dataReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, ...action.payload, loading: false };
    case 'FETCH_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}