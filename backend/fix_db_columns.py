import asyncio
from sqlalchemy import text
from app.config.database import engine

async def fix_columns():
    async with engine.begin() as conn:
        print("Checking and adding missing columns to business_processes and other tables...")
        cols_to_add = [
            ("business_processes", "name", "VARCHAR(255) DEFAULT 'Process Flow'"),
            ("business_processes", "description", "TEXT"),
            ("business_processes", "step_number", "INTEGER DEFAULT 1"),
            ("business_processes", "activity", "VARCHAR(255) DEFAULT ''"),
            ("business_processes", "actor", "VARCHAR(255) DEFAULT ''"),
            ("business_processes", "system", "VARCHAR(255) DEFAULT ''"),
            ("business_processes", "duration", "VARCHAR(100) DEFAULT ''"),
            ("business_processes", "is_bottleneck", "BOOLEAN DEFAULT FALSE"),
            ("business_processes", "pain_points", "JSONB DEFAULT '[]'::jsonb"),
            ("business_processes", "as_is_steps", "JSONB DEFAULT '[]'::jsonb"),
            ("business_processes", "to_be_steps", "JSONB DEFAULT '[]'::jsonb"),
            ("business_processes", "cycle_time_current", "VARCHAR(100)"),
            ("business_processes", "cycle_time_projected", "VARCHAR(100)"),
            ("business_processes", "bottlenecks", "JSONB DEFAULT '[]'::jsonb"),
            
            # Recommendation columns
            ("recommendations", "impact_score", "FLOAT DEFAULT 9.0"),
            ("recommendations", "feasibility_score", "FLOAT DEFAULT 8.5"),
            ("recommendations", "effort_score", "FLOAT DEFAULT 5.0"),
            ("recommendations", "cost_estimate", "FLOAT DEFAULT 25000.0"),
            ("recommendations", "roi_percentage", "FLOAT DEFAULT 350.0"),
            ("recommendations", "why_ai_rationale", "TEXT"),
            ("recommendations", "expected_outcome", "TEXT"),
            ("recommendations", "architecture_impact", "TEXT"),
            ("recommendations", "time_to_value_months", "INTEGER DEFAULT 3"),
            ("recommendations", "confidence_score", "FLOAT DEFAULT 0.94"),
            ("recommendations", "review_status", "VARCHAR(50) DEFAULT 'DRAFT'"),
            ("recommendations", "reviewed_by_ba_id", "VARCHAR(36)"),
            ("recommendations", "reviewed_by_arch_id", "VARCHAR(36)"),
            ("recommendations", "approved_by_id", "VARCHAR(36)"),
            ("recommendations", "ba_notes", "TEXT"),
            ("recommendations", "arch_notes", "TEXT"),
            ("recommendations", "approval_notes", "TEXT"),
        ]
        
        for table, col, col_type in cols_to_add:
            try:
                await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col} {col_type};"))
                print(f"  + Added column {table}.{col}")
            except Exception as e:
                print(f"  - Note on {table}.{col}: {e}")
                
        print("\nColumn sync completed!")

if __name__ == "__main__":
    asyncio.run(fix_columns())
