from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

def role_required(roles):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            access_token = get_access_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            user = get_current_user()
            # Get the user's roles
            roles = requests.get(f"https://graph.microsoft.com/v1.0/users/{user.id}/memberOf", headers=headers)
            roles = [role['displayName'] for role in roles.json()['value']]
            if user.role not in roles:
                raise HTTPException(status_code=400, detail="Not enough privileges")
            return await func(*args, **kwargs)
        return wrapper
    return decorator


@app.get("/admin-only")
@role_required(["admin"])
async def admin_only():
    return {"message": "Welcome, admin!"}

@app.get("/users")
@role_required(["admin", "user"])
async def users():
    return {"message": "Welcome, user!"}





# ---------------------------------------------------------------///-------------------------------------------------



# import requests

# def get_user_roles(user_id, access_token):
#     headers = {"Authorization": f"Bearer {access_token}"}
#     roles = requests.get(f"https://graph.microsoft.com/v1.0/users/{user_id}/memberOf", headers=headers)
#     roles = [role['displayName'] for role in roles.json()['value']]
#     return roles

# from fastapi import FastAPI, HTTPException

# app = FastAPI()


# def role_required(roles):
#     def decorator(func):
#         async def wrapper(*args, **kwargs):
#             access_token = get_access_token()
#             user_id = get_current_user_id()
#             user_roles = get_user_roles(user_id, access_token)
#             if not set(user_roles).intersection(roles):
#                 raise HTTPException(status_code=403, detail="Not enough privileges")
#             return await func(*args, **kwargs)
#         return wrapper
#     return decorator


