# Image-Quality-and-Defect-Detection

## Railway deployment

Deploy this repository as two Railway services, both using Docker:

1. Create a backend service with root directory `backend`.
2. Create a frontend service with root directory `frontend`.
3. Add backend variables: `DATABASE_URL`, `IMAGGA_API_KEY`, `IMAGGA_API_SECRET`, and `ALLOWED_ORIGINS`.
4. Set the frontend build variable `VITE_API_BASE_URL` to the public backend URL.
5. Set `ALLOWED_ORIGINS` to the public frontend URL.

Use managed Postgres for `DATABASE_URL` in production. Keep Imagga credentials in Railway variables, never in Git or frontend variables.