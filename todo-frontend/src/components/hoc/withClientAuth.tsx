"use client";

import { isAuthenticatedUser } from '@/lib/jwtHandlers';
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const withAuth = (Component: React.ComponentType) => {
  return function ProtectedComponent(props: any) {
    const router = useRouter();

    useEffect(() => {
      if (!isAuthenticatedUser) {
        router.push("/auth/login");
      }
    }, [router]);

    if (!isAuthenticatedUser) {
      return <div>Loading...</div>;
    }

    return <Component {...props} />;
  };
};

export default withAuth;
