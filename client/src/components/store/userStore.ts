import { create } from "zustand";
interface IUserDetails {
  username: String;
}

interface UserDetailsState {
  userDetails: IUserDetails | null;
  // user:IUserDetails | null;
  setUserDetails: (userDetails: IUserDetails | null) => void;
  // setUser: (user: IUserDetails) => void;
  error: boolean;
  setError: (error: boolean) => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  errorStatus: any;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  setErrorStatus: (errorStatus: any) => void;
}

// Assigning initial values to the Store and defining the properties.
export const userDetailsStore = create<UserDetailsState>((set) => ({
  userDetails: null,
  error: false,
  errorStatus: {},
  // user: null,
  setUserDetails: (userDetails: IUserDetails | null) => {
    set(() => ({ userDetails }));
  },
  // setUser: (user) => {
  //   set(() => ({ user }));
  // },
  setError: (error: boolean) => {
    set(() => ({ error }));
  },
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  setErrorStatus: (errorStatus: any) => {
    set(() => ({ errorStatus }));
  },
}));
