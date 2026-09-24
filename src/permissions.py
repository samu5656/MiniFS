class PermissionManager:
    @staticmethod
    def check_access(permissions, owner, user, operation):
        """
        Check if the user has the required permission for the operation.
        permissions: str (e.g., 'rw-r--r--')
        owner: str
        user: str
        operation: 'read', 'write', 'execute'
        """
        if len(permissions) != 9:
            return False
            
        owner_perms = permissions[0:3]
        group_perms = permissions[3:6]
        others_perms = permissions[6:9]
        
        # Simplified check: if user is the owner, check owner perms, else check others perms
        # (Assuming no explicit group management for this simulation)
        active_perms = owner_perms if user == owner else others_perms
        
        if operation == "read" and active_perms[0] == 'r': return True
        if operation == "write" and active_perms[1] == 'w': return True
        if operation == "execute" and active_perms[2] == 'x': return True
        
        return False
