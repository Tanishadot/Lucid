# Conversation Persistence Setup Guide

This guide explains how to set up and test the conversation persistence feature for the ReflectionJourney app.

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Setup

The app uses PostgreSQL. You need to set up a PostgreSQL database and update the `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/lucid_db
```

### 3. Initialize Database

```bash
python init_db.py
```

### 4. Start Backend Server

```bash
python main.py
```

The server will start on `http://localhost:8000` and automatically create the database tables.

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Frontend Server

```bash
npm run dev
```

The frontend will start on `http://localhost:5173` (or similar).

## Testing the API

### Backend API Test

Run the test script to verify all endpoints work:

```bash
cd backend
python test_conversation_api.py
```

This will test:
- Creating conversations
- Adding messages
- Retrieving conversations
- Listing all conversations

## API Endpoints

### Conversations

- `GET /api/conversations` - Get all conversations for user
- `GET /api/conversations/{id}` - Get conversation with messages
- `POST /api/conversations` - Create new conversation
- `POST /api/conversations/start` - Start conversation with first message
- `POST /api/conversations/{id}/messages` - Add message to conversation
- `DELETE /api/conversations/{id}` - Delete conversation

### Database Schema

#### Conversations Table
- `id` (UUID, primary key)
- `user_id` (UUID, indexed)
- `title` (string, auto-generated)
- `created_at` (timestamp)
- `updated_at` (timestamp)

#### Messages Table
- `id` (UUID, primary key)
- `conversation_id` (foreign key)
- `role` (enum: "user" | "assistant")
- `content` (text)
- `timestamp` (timestamp)

## Features Implemented

### Backend
✅ Database models for conversations and messages
✅ Async database service layer
✅ REST API endpoints with proper error handling
✅ User authentication (mock implementation)
✅ Automatic title generation from first message
✅ Conversation timestamp updates

### Frontend
✅ Conversation sidebar with list of conversations
✅ TypeScript types for all data structures
✅ API service layer with error handling
✅ Conversation persistence in chat interface
✅ Loading states and error handling
✅ Responsive sidebar with toggle
✅ Conversation deletion functionality

## Usage

1. **Starting a New Conversation**: Simply type a message and send it. A new conversation will be automatically created.

2. **Viewing Past Conversations**: Click on any conversation in the sidebar to load its message history.

3. **Creating a New Conversation**: Click the "+" button in the sidebar header.

4. **Deleting Conversations**: Hover over a conversation in the sidebar and click the trash icon.

5. **Toggle Sidebar**: Use the arrow button next to the header to show/hide the sidebar.

## Security Notes

- The current implementation uses mock user authentication
- In production, implement proper JWT-based authentication
- Row-level security should be implemented in the database
- All API endpoints should validate user permissions

## Development Notes

- The backend uses SQLAlchemy with async support
- PostgreSQL is the recommended database
- The frontend uses React with TypeScript
- State management is handled with React hooks
- API calls use Axios with proper error handling

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check the DATABASE_URL in .env file
- Verify database permissions

### API Connection Issues
- Ensure backend server is running on port 8000
- Check CORS settings in main.py
- Verify frontend API URL configuration

### Frontend Issues
- Check browser console for errors
- Ensure all dependencies are installed
- Verify TypeScript compilation
