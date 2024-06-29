import { create } from "zustand";
interface IUserDetails {
  username: string;
  password: string | undefined;
  userId?: number | undefined;
  dataProfileId?: number | undefined;
}

interface UserDetailsState {
  userDetails: IUserDetails | null;
  setUserDetails: (userDetails: IUserDetails | null) => void;
  error: boolean;
  setError: (error: boolean) => void;
  errorStatus: any;
  setErrorStatus: (errorStatus: any) => void;
}

export const userDetailsStore = create<UserDetailsState>((set) => ({
  userDetails: null,
  error: false,
  errorStatus: {},
  setUserDetails: (userDetails: IUserDetails | null) => {
    set(() => ({ userDetails }));
  },
  setError: (error: boolean) => {
    set(() => ({ error }));
  },
  setErrorStatus: (errorStatus: any) => {
    set(() => ({ errorStatus }));
  },
}));
